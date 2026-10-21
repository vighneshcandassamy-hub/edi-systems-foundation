"""C0-only durable orchestration, exact staged requests and attempt fencing."""
from contextlib import contextmanager
from hashlib import sha256
import json
import shutil
import sqlite3

from edi.shared.contracts import utc_now
from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    value = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def hashed(value): return sha256(canonical(value).encode("utf-8")).hexdigest()


class SQLiteWorkflowStore:
    def __init__(self, profile):
        self.profile, self.path = profile, profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C0 workflow database")
                con.execute("CREATE TABLE info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace TEXT NOT NULL, records INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0)")
                con.execute("CREATE TABLE plans (workflow TEXT PRIMARY KEY, digest TEXT NOT NULL, document TEXT NOT NULL, semantic_profile TEXT NOT NULL, cancelled INTEGER NOT NULL DEFAULT 0)")
                con.execute("CREATE TABLE inputs (workflow TEXT NOT NULL, input_id TEXT NOT NULL, digest TEXT NOT NULL, document TEXT NOT NULL, PRIMARY KEY(workflow,input_id))")
                con.execute("CREATE TABLE steps (workflow TEXT NOT NULL, step_id TEXT NOT NULL, attempt INTEGER NOT NULL, state TEXT NOT NULL, arguments TEXT NOT NULL, arguments_sha256 TEXT NOT NULL, result TEXT, result_sha256 TEXT, error TEXT, started_at TEXT NOT NULL, elapsed REAL, completion_limit INTEGER NOT NULL, PRIMARY KEY(workflow,step_id))")
                con.execute("CREATE TABLE attempts (workflow TEXT NOT NULL, step_id TEXT NOT NULL, attempt INTEGER NOT NULL, started_at TEXT NOT NULL, state TEXT NOT NULL, elapsed REAL, PRIMARY KEY(workflow,step_id,attempt))")
                con.execute("INSERT INTO info(singleton,workspace) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1: raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C0 workflow schema")
            if con.execute("SELECT workspace FROM info WHERE singleton=1").fetchone()[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C0 workflow workspace differs")
            self.commit(con)

    @contextmanager
    def connection(self):
        con = None
        try:
            con = sqlite3.connect(self.path, timeout=self.profile.writer_timeout_seconds, isolation_level=None)
            con.execute("PRAGMA synchronous=FULL")
            con.execute("PRAGMA cache_size=-4096")
            yield con
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.STORAGE, f"C0 workflow storage unavailable: {exc}", retryable=True) from exc
        finally:
            if con is not None:
                try:
                    if con.in_transaction: con.rollback()
                finally: con.close()

    @staticmethod
    def commit(con):
        try: con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C0 workflow commit unknown; query original plan/step", retryable=True) from exc

    def reserve(self, con, amount, count=1):
        records, used = con.execute("SELECT records,bytes FROM info WHERE singleton=1").fetchone()
        if used + amount > self.profile.max_stored_bytes or records + count > self.profile.max_records:
            raise EDIError(ErrorCode.CAPACITY, "C0 workflow quota reached")
        if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C0 workflow disk reserve reached", retryable=True)
        con.execute("UPDATE info SET records=records+?,bytes=bytes+? WHERE singleton=1", (count, amount))

    def create(self, spec):
        encoded, digest = canonical(spec), hashed(spec)
        semantic = self.semantic_profile()
        if len(encoded.encode("utf-8")) > self.profile.max_plan_bytes: raise EDIError(ErrorCode.CAPACITY, "workflow plan too large")
        with self.connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT digest,semantic_profile FROM plans WHERE workflow=?", (spec.workflow_id,)).fetchone()
            if row:
                if row != (digest, semantic): raise EDIError(ErrorCode.CONFLICT, "workflow plan or authority profile differs")
                return digest
            self.reserve(con, len(encoded.encode("utf-8")))
            con.execute("INSERT INTO plans(workflow,digest,document,semantic_profile) VALUES(?,?,?,?)", (spec.workflow_id, digest, encoded, semantic))
            self.commit(con)
            return digest

    def load(self, workflow_id):
        with self.connection() as con:
            con.execute("BEGIN")
            row = con.execute("SELECT digest,document,semantic_profile,cancelled FROM plans WHERE workflow=?", (workflow_id,)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, "workflow unavailable")
            semantic = self.semantic_profile()
            if row[2] != semantic: raise EDIError(ErrorCode.CONFLICT, "workflow authority profile changed; create a new workflow")
            spec = json.loads(row[1])
            if hashed(spec) != row[0]: raise EDIError(ErrorCode.INTEGRITY, "workflow plan digest differs")
            inputs = {r[0] for r in con.execute("SELECT input_id FROM inputs WHERE workflow=?", (workflow_id,))}
            steps = {key: {"attempt": attempt, "state": state, "result_sha256": result_hash, "error": json.loads(error) if error is not None else None, "elapsed_seconds": elapsed}
                for key, attempt, state, result_hash, error, elapsed in con.execute("SELECT step_id,attempt,state,result_sha256,error,elapsed FROM steps WHERE workflow=?", (workflow_id,))}
            return spec, row[0], inputs, steps, bool(row[3])

    def selected(self, workflow_id, kind, key):
        with self.connection() as con:
            if kind in ("input", "input-record"):
                row = con.execute("SELECT document,digest FROM inputs WHERE workflow=? AND input_id=?", (workflow_id, key)).fetchone()
            elif kind == "arguments":
                row = con.execute("SELECT arguments,arguments_sha256 FROM steps WHERE workflow=? AND step_id=?", (workflow_id, key)).fetchone()
            elif kind == "result":
                row = con.execute("SELECT result,result_sha256 FROM steps WHERE workflow=? AND step_id=? AND state IN ('completed','failed')", (workflow_id, key)).fetchone()
            else: raise EDIError(ErrorCode.INVALID, "unknown C0 selection kind")
            if row is None or row[0] is None: raise EDIError(ErrorCode.NOT_FOUND, "workflow selection unavailable")
            value = json.loads(row[0])
            if hashed(value) != row[1]: raise EDIError(ErrorCode.INTEGRITY, "workflow selection hash differs")
            return value["value"] if kind == "input" else value

    def semantic_profile(self):
        return canonical({"profile_id": self.profile.profile_id,
            "trusted_operator_steps": self.profile.trusted_operator_steps,
            "operator_ids": self.profile.operator_ids})

    def supply(self, request):
        encoded, digest = canonical(request), hashed(request)
        if len(encoded.encode("utf-8")) > self.profile.max_input_bytes: raise EDIError(ErrorCode.CAPACITY, "workflow input too large")
        with self.connection() as con:
            con.execute("BEGIN IMMEDIATE")
            if con.execute("SELECT 1 FROM plans WHERE workflow=?", (request.workflow_id,)).fetchone() is None:
                raise EDIError(ErrorCode.NOT_FOUND, "workflow unavailable")
            prior = con.execute("SELECT digest FROM inputs WHERE workflow=? AND input_id=?", (request.workflow_id, request.input_id)).fetchone()
            if prior:
                if prior[0] != digest: raise EDIError(ErrorCode.CONFLICT, "workflow input is immutable")
                return
            self.reserve(con, len(encoded.encode("utf-8")))
            con.execute("INSERT INTO inputs VALUES(?,?,?,?)", (request.workflow_id, request.input_id, digest, encoded))
            self.commit(con)

    def begin(self, workflow_id, step_id, arguments, *, retry_uncertain=False):
        encoded = canonical(arguments)
        amount = len(encoded.encode("utf-8"))
        if amount > self.profile.max_step_bytes: raise EDIError(ErrorCode.CAPACITY, "resolved workflow arguments too large")
        with self.connection() as con:
            con.execute("BEGIN IMMEDIATE")
            if con.execute("SELECT cancelled FROM plans WHERE workflow=?", (workflow_id,)).fetchone()[0]:
                raise EDIError(ErrorCode.DENIED, "workflow cancelled")
            row = con.execute("SELECT attempt,state,arguments FROM steps WHERE workflow=? AND step_id=?", (workflow_id, step_id)).fetchone()
            if row:
                if row[1] != "pending" or not retry_uncertain: return None
                if row[2] != encoded: raise EDIError(ErrorCode.CONFLICT, "uncertain workflow step arguments changed")
                self.reserve(con, 1024)
                attempt = row[0] + 1
                con.execute("UPDATE attempts SET state='superseded-usage-unknown' WHERE workflow=? AND step_id=? AND attempt=?", (workflow_id, step_id, row[0]))
                con.execute("UPDATE steps SET attempt=?,started_at=? WHERE workflow=? AND step_id=?", (attempt, utc_now().isoformat(), workflow_id, step_id))
            else:
                if con.execute("SELECT 1 FROM steps WHERE workflow=? AND state='pending'", (workflow_id,)).fetchone():
                    raise EDIError(ErrorCode.CONFLICT, "workflow already has an unresolved step")
                self.reserve(con, amount + self.profile.max_step_bytes + 8192, 2)
                attempt = 1
                con.execute("INSERT INTO steps(workflow,step_id,attempt,state,arguments,arguments_sha256,started_at,completion_limit) VALUES(?,?,?,'pending',?,?,?,?)", (workflow_id, step_id, attempt, encoded, hashed(arguments), utc_now().isoformat(), self.profile.max_step_bytes + 8192))
            con.execute("INSERT INTO attempts(workflow,step_id,attempt,started_at,state) VALUES(?,?,?,?,'pending-usage-unknown')", (workflow_id, step_id, attempt, utc_now().isoformat()))
            self.commit(con)
            return attempt

    def finish(self, workflow_id, step_id, attempt, result, error, elapsed):
        output = canonical(result)
        diagnostic = canonical(error) if error is not None else None
        with self.connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT attempt,state,completion_limit FROM steps WHERE workflow=? AND step_id=?", (workflow_id, step_id)).fetchone()
            if row is None or row[:2] != (attempt, "pending"):
                raise EDIError(ErrorCode.CONFLICT, "workflow step lost its attempt fence")
            if len((output + (diagnostic or "")).encode("utf-8")) > row[2]:
                raise EDIError(ErrorCode.CAPACITY, "workflow completion exceeds original allowance; step remains unresolved")
            con.execute("UPDATE steps SET state=?,result=?,result_sha256=?,error=?,elapsed=? WHERE workflow=? AND step_id=?", ("failed" if error else "completed", output, hashed(result), diagnostic, elapsed, workflow_id, step_id))
            con.execute("UPDATE attempts SET state=?,elapsed=? WHERE workflow=? AND step_id=? AND attempt=?", ("failed" if error else "completed", elapsed, workflow_id, step_id, attempt))
            self.commit(con)

    def attempts(self, workflow_id, step_id, *, after=0, limit=25):
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 100:
            raise EDIError(ErrorCode.INVALID, "invalid C0 attempt selection")
        with self.connection() as con:
            rows = con.execute("SELECT attempt,started_at,state,elapsed FROM attempts WHERE workflow=? AND step_id=? AND attempt>? ORDER BY attempt LIMIT ?", (workflow_id, step_id, after, limit + 1)).fetchall()
            items = [{"attempt": a, "started_at": t, "state": s, "elapsed_seconds": e} for a,t,s,e in rows[:limit]]
            return {"items": items, "next_after": items[-1]["attempt"] if len(rows) > limit else None,
                "usage_limit": "superseded attempts retain unknown usage; local elapsed excludes paused time and does not measure model/energy cost"}

    def cancel(self, workflow_id):
        with self.connection() as con:
            con.execute("BEGIN IMMEDIATE")
            if con.execute("SELECT 1 FROM steps WHERE workflow=? AND state='pending'", (workflow_id,)).fetchone():
                raise EDIError(ErrorCode.CONFLICT, "reconcile unresolved step before cancelling")
            if con.execute("UPDATE plans SET cancelled=1 WHERE workflow=?", (workflow_id,)).rowcount != 1:
                raise EDIError(ErrorCode.NOT_FOUND, "workflow unavailable")
            self.commit(con)
