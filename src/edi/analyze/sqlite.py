"""C5 immutable compiled artifacts and fenced run intents/results."""
from contextlib import contextmanager
import json
import shutil
import sqlite3

from edi.analyze.contracts import CompiledModel, RunRecord
from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    value = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SQLiteAnalysisStore:
    def __init__(self, profile):
        self.profile, self.path = profile, profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C5 database")
                for sql in (
                    "CREATE TABLE analysis_info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL, records INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0)",
                    "CREATE TABLE compiled (request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, compiled_id TEXT NOT NULL UNIQUE, document TEXT NOT NULL)",
                    "CREATE TABLE runs (request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, run_id TEXT NOT NULL UNIQUE, attempt TEXT NOT NULL, active INTEGER NOT NULL, cancel INTEGER NOT NULL DEFAULT 0, reason TEXT, intent TEXT NOT NULL, result TEXT)",
                    "CREATE UNIQUE INDEX one_analysis_worker ON runs(active) WHERE active=1",
                    "CREATE TABLE controls (request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, run_request_id TEXT NOT NULL, document TEXT NOT NULL)",
                    "CREATE INDEX control_target ON controls(run_request_id)",
                ):
                    con.execute(sql)
                con.execute("INSERT INTO analysis_info(singleton,workspace_id) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C5 schema")
            row = con.execute("SELECT workspace_id FROM analysis_info WHERE singleton=1").fetchone()
            if row is None or row[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C5 workspace mismatch")
            self._commit(con)

    @contextmanager
    def _connection(self):
        con = None
        try:
            con = sqlite3.connect(self.path, timeout=self.profile.writer_timeout_seconds, isolation_level=None)
            con.execute("PRAGMA synchronous=FULL")
            con.execute("PRAGMA cache_size=-4096")
            yield con
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.STORAGE, f"C5 storage unavailable: {exc}", retryable=True) from exc
        finally:
            if con is not None:
                try:
                    if con.in_transaction: con.rollback()
                finally:
                    con.close()

    @staticmethod
    def _commit(con):
        try: con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C5 commit outcome unknown; query original request", retryable=True) from exc

    def _reserve(self, con, size):
        count, used = con.execute("SELECT records,bytes FROM analysis_info WHERE singleton=1").fetchone()
        if count >= self.profile.max_records or used + size > self.profile.max_stored_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C5 retained artifact quota reached")
        if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C5 disk reserve reached", retryable=True)
        con.execute("UPDATE analysis_info SET records=records+1,bytes=bytes+? WHERE singleton=1", (size,))

    def find_compile(self, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,document FROM compiled WHERE request_id=?", (request_id,)).fetchone()
            if row is None: return None
            if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C5 compile identity changed")
            return CompiledModel.model_validate_json(row[1])

    def get_compiled(self, compiled_id):
        with self._connection() as con:
            row = con.execute("SELECT document FROM compiled WHERE compiled_id=?", (compiled_id,)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, "C5 compiled artifact unavailable")
            return CompiledModel.model_validate_json(row[0])

    def save_compile(self, fingerprint, compiled):
        encoded = canonical(compiled)
        size = len(encoded.encode("utf-8"))
        if size > self.profile.max_result_bytes: raise EDIError(ErrorCode.CAPACITY, "compiled artifact exceeds result limit")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT fingerprint,document FROM compiled WHERE request_id=?", (compiled.request.request_id,)).fetchone()
            if row is not None:
                if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C5 compile retry differs")
                return CompiledModel.model_validate_json(row[1])
            self._reserve(con, size)
            con.execute("INSERT INTO compiled VALUES(?,?,?,?)", (compiled.request.request_id, fingerprint, compiled.compiled_id, encoded))
            self._commit(con)
            return CompiledModel.model_validate_json(encoded)

    def prepare_run(self, request, fingerprint, attempt, intent):
        encoded = canonical(intent)
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT fingerprint,result FROM runs WHERE request_id=?", (request.request_id,)).fetchone()
            if row is not None:
                if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C5 run request/binding changed")
                if row[1] is not None: return RunRecord.model_validate_json(row[1])
                raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C5 run intent exists without final result; query/cancel/fence, never auto-repeat")
            if con.execute("SELECT request_id FROM runs WHERE active=1").fetchone():
                raise EDIError(ErrorCode.CAPACITY, "one active C5 run per workspace", retryable=True)
            # Reserve terminal result and sixteen bounded control receipts up front.
            self._reserve(con, len(encoded.encode("utf-8")) + self.profile.max_result_bytes + 256 * 1024)
            con.execute("INSERT INTO runs(request_id,fingerprint,run_id,attempt,active,intent) VALUES(?,?,?,?,1,?)", (request.request_id, fingerprint, request.run_id, attempt, encoded))
            self._commit(con)
            return None

    def find_run(self, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,result FROM runs WHERE request_id=?", (request_id,)).fetchone()
            if row is None: return None
            if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C5 original run identity changed")
            if row[1] is None: raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C5 intent unresolved; query/cancel/fence before a new request")
            return RunRecord.model_validate_json(row[1])

    def status(self, request_id):
        with self._connection() as con:
            row = con.execute("SELECT run_id,attempt,active,cancel,reason,result FROM runs WHERE request_id=?", (request_id,)).fetchone()
            if row is None: return None
            return {"request_id": request_id, "run_id": row[0], "attempt": row[1], "active": bool(row[2]),
                    "cancel_requested": bool(row[3]), "control_reason": row[4],
                    "status": json.loads(row[5])["status"] if row[5] is not None else "running-or-interrupted; reconcile explicitly"}

    def intent(self, request_id):
        with self._connection() as con:
            row = con.execute("SELECT intent FROM runs WHERE request_id=?", (request_id,)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, "C5 run intent unavailable")
            return json.loads(row[0])

    def get_run(self, run_id):
        with self._connection() as con:
            row = con.execute("SELECT result FROM runs WHERE run_id=?", (run_id,)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, "C5 run unavailable")
            if row[0] is None: raise EDIError(ErrorCode.INCOMPLETE, "C5 run has no final immutable result")
            return RunRecord.model_validate_json(row[0])

    def cancelled(self, request_id, attempt):
        with self._connection() as con:
            row = con.execute("SELECT attempt,active,cancel FROM runs WHERE request_id=?", (request_id,)).fetchone()
            return row is None or row[0] != attempt or not row[1] or bool(row[2])

    def finish(self, request_id, attempt, result):
        encoded = canonical(result)
        if len(encoded.encode("utf-8")) > self.profile.max_result_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C5 result exceeds reserved artifact bound")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT attempt,result,cancel,intent FROM runs WHERE request_id=?", (request_id,)).fetchone()
            if row is None or row[0] != attempt: raise EDIError(ErrorCode.CONFLICT, "C5 worker fenced; no stale result admission")
            if row[1] is not None: return RunRecord.model_validate_json(row[1])
            if len(encoded.encode("utf-8")) > json.loads(row[3])["profile"]["max_result_bytes"]:
                raise EDIError(ErrorCode.CAPACITY, "C5 result exceeds its original reserved byte budget")
            if row[2] and result.status not in ("cancelled", "interrupted"):
                raise EDIError(ErrorCode.CONFLICT, "C5 cancellation arrived before result commit; reconcile explicitly")
            con.execute("UPDATE runs SET result=?,active=0 WHERE request_id=?", (encoded, request_id))
            self._commit(con)
            return RunRecord.model_validate_json(encoded)

    def control(self, request, fingerprint, replacement_attempt=None):
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = con.execute("SELECT fingerprint,document FROM controls WHERE request_id=?", (request.request_id,)).fetchone()
            if previous is not None:
                if previous[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C5 control request changed")
                return json.loads(previous[1])
            row = con.execute("SELECT attempt,result FROM runs WHERE request_id=?", (request.run_request_id,)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, "C5 controlled run unavailable")
            if row[1] is not None: raise EDIError(ErrorCode.CONFLICT, "C5 final result is immutable")
            if request.action == "interrupt":
                if request.expected_attempt != row[0]: raise EDIError(ErrorCode.CONFLICT, "C5 expected worker identity differs")
                con.execute("UPDATE runs SET attempt=?,cancel=1,reason=? WHERE request_id=?", (replacement_attempt, request.reason, request.run_request_id))
            else:
                con.execute("UPDATE runs SET cancel=1,reason=? WHERE request_id=?", (request.reason, request.run_request_id))
            document = request.model_dump(mode="json") | {"replacement_attempt": replacement_attempt}
            encoded = canonical(document)
            if len(encoded.encode("utf-8")) > 16 * 1024 or con.execute("SELECT COUNT(*) FROM controls WHERE run_request_id=?", (request.run_request_id,)).fetchone()[0] >= 16:
                raise EDIError(ErrorCode.CAPACITY, "C5 reserved control receipt limit reached")
            con.execute("INSERT INTO controls VALUES(?,?,?,?)", (request.request_id, fingerprint, request.run_request_id, encoded))
            self._commit(con)
            return document
