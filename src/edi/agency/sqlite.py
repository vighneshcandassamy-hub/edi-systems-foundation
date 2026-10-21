"""C7-only append-only artifacts, policy CAS and prepaid command completion."""
from contextlib import contextmanager
import json
import shutil
import sqlite3

from edi.agency.contracts import ArtifactCursor, ArtifactPage
from edi.shared.contracts import utc_now
from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    value = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


class SQLiteAgencyStore:
    def __init__(self, profile):
        self.profile, self.path = profile, profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C7 database")
                con.execute("CREATE TABLE agency_info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL, records INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0, policy_revision INTEGER NOT NULL DEFAULT 0, active_execution TEXT)")
                con.execute("CREATE TABLE artifacts (position INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, artifact_id TEXT NOT NULL, request_id TEXT NOT NULL, fingerprint TEXT NOT NULL, scope_key TEXT, completion_limit INTEGER NOT NULL DEFAULT 0, document TEXT NOT NULL, UNIQUE(kind,artifact_id), UNIQUE(kind,request_id))")
                con.execute("CREATE INDEX artifact_selection ON artifacts(kind,position)")
                con.execute("CREATE INDEX artifact_scope ON artifacts(kind,scope_key,position)")
                con.execute("CREATE UNIQUE INDEX consumed_decision ON artifacts(json_extract(document,'$.decision.request.decision_id')) WHERE kind='execution-intent'")
                con.execute("CREATE UNIQUE INDEX terminal_amendment ON artifacts(json_extract(document,'$.request.amendment_id')) WHERE kind='adoption' AND json_extract(document,'$.request.decision') IN ('adopt','reject')")
                con.execute("CREATE INDEX adopted_purpose ON artifacts(json_extract(document,'$.policy.purpose_version')) WHERE kind='adoption' AND json_extract(document,'$.request.decision')='adopt'")
                con.execute("CREATE TABLE policy_versions (revision INTEGER PRIMARY KEY, adoption_id TEXT NOT NULL)")
                con.execute("INSERT INTO agency_info(singleton,workspace_id) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C7 schema")
            row = con.execute("SELECT workspace_id FROM agency_info WHERE singleton=1").fetchone()
            if row is None or row[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C7 database workspace differs")
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
            raise EDIError(ErrorCode.STORAGE, f"C7 storage unavailable: {exc}", retryable=True) from exc
        finally:
            if con is not None:
                try:
                    if con.in_transaction: con.rollback()
                finally: con.close()

    @staticmethod
    def _commit(con):
        try: con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C7 commit outcome unknown; query original request", retryable=True) from exc

    @staticmethod
    def _previous(con, kind, artifact_id, request_id, fingerprint):
        rows = con.execute("SELECT artifact_id,request_id,fingerprint,document FROM artifacts WHERE kind=? AND (artifact_id=? OR request_id=?)", (kind, artifact_id, request_id)).fetchall()
        if not rows: return None
        if len(rows) != 1 or rows[0][:3] != (artifact_id, request_id, fingerprint):
            raise EDIError(ErrorCode.CONFLICT, "C7 artifact/request identity or payload differs")
        return json.loads(rows[0][3])

    def find(self, kind, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,document FROM artifacts WHERE kind=? AND request_id=?", (kind, request_id)).fetchone()
            if row is None: return None
            if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C7 request identity reused with changed payload")
            return json.loads(row[1])

    def get(self, kind, artifact_id):
        with self._connection() as con:
            row = con.execute("SELECT document FROM artifacts WHERE kind=? AND artifact_id=?", (kind, artifact_id)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, f"C7 {kind} artifact unavailable")
            return json.loads(row[0])

    def optional(self, kind, artifact_id):
        try: return self.get(kind, artifact_id)
        except EDIError as exc:
            if exc.code == ErrorCode.NOT_FOUND: return None
            raise

    def latest_scope(self, kind, scope_key):
        with self._connection() as con:
            row = con.execute("SELECT document FROM artifacts WHERE kind=? AND scope_key=? ORDER BY position DESC LIMIT 1", (kind, scope_key)).fetchone()
            return json.loads(row[0]) if row else None

    def _insert(self, con, kind, artifact_id, request_id, fingerprint, document, *, scope_key=None):
        encoded = canonical(document)
        amount = len(encoded.encode("utf-8"))
        if amount > self.profile.max_document_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C7 document byte limit exceeded")
        parents = {"execution-receipt": "execution-intent", "report-archive": "report-stage", "model-receipt": "model-stage"}
        completion_limit = 0
        if kind in parents:
            parent = con.execute("SELECT completion_limit FROM artifacts WHERE kind=? AND artifact_id=?", (parents[kind], artifact_id)).fetchone()
            if parent is None:
                raise EDIError(ErrorCode.INVALID, "C7 completion has no prepaid parent")
            if amount > parent[0]:
                raise EDIError(ErrorCode.CAPACITY, "C7 completion exceeds its original prepaid byte allowance")
            # The parent reserved one maximum-sized completion document and row.
        else:
            count, used = con.execute("SELECT records,bytes FROM agency_info WHERE singleton=1").fetchone()
            reserved = kind in ("execution-intent", "report-stage", "model-stage")
            rows, extra = (2, self.profile.max_document_bytes) if reserved else (1, 0)
            completion_limit = extra
            if count + rows > self.profile.max_records or used + amount + extra > self.profile.max_stored_bytes:
                raise EDIError(ErrorCode.CAPACITY, "C7 retained-artifact quota reached")
            if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
                raise EDIError(ErrorCode.CAPACITY, "C7 disk reserve reached", retryable=True)
            con.execute("UPDATE agency_info SET records=records+?,bytes=bytes+? WHERE singleton=1", (rows, amount + extra))
        con.execute("INSERT INTO artifacts(kind,artifact_id,request_id,fingerprint,scope_key,completion_limit,document) VALUES(?,?,?,?,?,?,?)", (kind, artifact_id, request_id, fingerprint, scope_key, completion_limit, encoded))
        return json.loads(encoded)

    def put(self, kind, artifact_id, request_id, fingerprint, document, *, scope_key=None):
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = self._previous(con, kind, artifact_id, request_id, fingerprint)
            if previous is not None: return previous
            result = self._insert(con, kind, artifact_id, request_id, fingerprint, document, scope_key=scope_key)
            self._commit(con)
            return result

    def policy(self, revision=None):
        with self._connection() as con:
            con.execute("BEGIN")
            high = con.execute("SELECT policy_revision FROM agency_info WHERE singleton=1").fetchone()[0]
            if revision is not None and (type(revision) is not int or revision < 1 or revision > high):
                raise EDIError(ErrorCode.NOT_FOUND, "C7 policy revision unavailable")
            cut = high if revision is None else revision
            if cut == 0: return None
            row = con.execute("SELECT a.document FROM policy_versions p JOIN artifacts a ON a.kind='adoption' AND a.artifact_id=p.adoption_id WHERE p.revision=?", (cut,)).fetchone()
            if row is None: raise EDIError(ErrorCode.INTEGRITY, "C7 policy history missing")
            return {"workspace_id": self.profile.workspace_id, "revision": cut, "adoption": json.loads(row[0])}

    def adopt(self, document, fingerprint):
        request = document.request
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = self._previous(con, "adoption", request.request_id, request.request_id, fingerprint)
            if previous is not None: return previous
            head, active = con.execute("SELECT policy_revision,active_execution FROM agency_info WHERE singleton=1").fetchone()
            if head != request.expected_revision:
                raise EDIError(ErrorCode.CONFLICT, "C7 adoption base policy changed")
            if request.decision == "adopt" and active is not None:
                raise EDIError(ErrorCode.CONFLICT, "resolve active/uncertain command before adopting another policy")
            prior = con.execute("SELECT document FROM artifacts WHERE kind='adoption' AND json_extract(document,'$.request.amendment_id')=? AND json_extract(document,'$.request.decision') IN ('adopt','reject') LIMIT 1", (request.amendment_id,)).fetchone()
            if prior is not None:
                raise EDIError(ErrorCode.CONFLICT, "C7 amendment already has a terminal decision; propose a new amendment")
            if request.decision == "adopt":
                historical = con.execute("SELECT document FROM artifacts WHERE kind='adoption' AND json_extract(document,'$.request.decision')='adopt' AND json_extract(document,'$.policy.purpose_version')=? LIMIT 1", (document.policy.purpose_version,)).fetchone()
                if historical is not None:
                    old = json.loads(historical[0])["policy"]
                    if (old["purpose"], old["evaluation_standards"]) != (document.policy.purpose, list(document.policy.evaluation_standards)):
                        raise EDIError(ErrorCode.CONFLICT, "C7 purpose version already names different historical standards")
            result = self._insert(con, "adoption", request.request_id, request.request_id, fingerprint, document)
            if request.decision == "adopt":
                if document.revision != head + 1: raise EDIError(ErrorCode.INTEGRITY, "C7 adoption revision mismatch")
                con.execute("INSERT INTO policy_versions(revision,adoption_id) VALUES(?,?)", (document.revision, request.request_id))
                con.execute("UPDATE agency_info SET policy_revision=? WHERE singleton=1", (document.revision,))
            self._commit(con)
            return result

    def begin_execution(self, document, fingerprint, now):
        request = document.request
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = self._previous(con, "execution-intent", request.execution_id, request.request_id, fingerprint)
            if previous is not None: return previous, False
            head, active = con.execute("SELECT policy_revision,active_execution FROM agency_info WHERE singleton=1").fetchone()
            if head != document.decision.request.policy_revision:
                raise EDIError(ErrorCode.CONFLICT, "C7 dispatch policy changed")
            if active is not None:
                raise EDIError(ErrorCode.CONFLICT, "another C7 command is active/unresolved; reconcile it first")
            now = utc_now()  # Sample after writer-lock acquisition, not before a possibly long wait.
            if now >= document.decision.expires_at or now < document.decision.created_at:
                raise EDIError(ErrorCode.DENIED, "C7 authorization expired or local clock regressed")
            row = con.execute("SELECT 1 FROM artifacts WHERE kind='execution-intent' AND json_extract(document,'$.decision.request.decision_id')=? LIMIT 1", (request.decision_id,)).fetchone()
            if row: raise EDIError(ErrorCode.CONFLICT, "C7 decision already consumed by another command")
            result = self._insert(con, "execution-intent", request.execution_id, request.request_id, fingerprint, document)
            con.execute("UPDATE agency_info SET active_execution=? WHERE singleton=1", (request.execution_id,))
            self._commit(con)
            return result, True

    def assert_execution(self, execution_id, revision):
        with self._connection() as con:
            head, active = con.execute("SELECT policy_revision,active_execution FROM agency_info WHERE singleton=1").fetchone()
            if active != execution_id or head != revision:
                raise EDIError(ErrorCode.CONFLICT, "C7 command lost its execution/policy fence")

    def finish_execution(self, document, request_id, fingerprint):
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = self._previous(con, "execution-receipt", document.execution_id, request_id, fingerprint)
            if previous is not None: return previous
            active = con.execute("SELECT active_execution FROM agency_info WHERE singleton=1").fetchone()[0]
            if active != document.execution_id:
                raise EDIError(ErrorCode.CONFLICT, "C7 command is no longer the unresolved execution")
            result = self._insert(con, "execution-receipt", document.execution_id, request_id, fingerprint, document)
            con.execute("UPDATE agency_info SET active_execution=NULL WHERE singleton=1")
            self._commit(con)
            return result

    def query(self, kind, *, cursor=None, limit=25):
        supported = ("amendment", "adoption", "decision", "execution-intent", "execution-receipt", "actor-view", "access", "access-disposition", "report-archive", "model-receipt")
        if kind not in supported or type(limit) is not int or not 1 <= limit <= 100:
            raise EDIError(ErrorCode.INVALID, "C7 artifact selection unsupported")
        if cursor is not None and (cursor.workspace_id != self.profile.workspace_id or cursor.kind != kind or cursor.after > cursor.watermark):
            raise EDIError(ErrorCode.DENIED, "C7 cursor scope/selection differs")
        with self._connection() as con:
            con.execute("BEGIN")
            high = con.execute("SELECT COALESCE(MAX(position),0) FROM artifacts").fetchone()[0]
            watermark, after = (high, 0) if cursor is None else (cursor.watermark, cursor.after)
            if watermark > high: raise EDIError(ErrorCode.INVALID, "C7 selection exceeds retained history")
            rows = con.execute("SELECT position,document FROM artifacts WHERE kind=? AND position>? AND position<=? ORDER BY position LIMIT ?", (kind, after, watermark, limit + 1))
            items, size, last, more = [], 0, after, False
            for pos, document in rows:
                amount = len(document.encode("utf-8"))
                if len(items) >= limit or size + amount > self.profile.max_page_bytes:
                    if not items: raise EDIError(ErrorCode.CAPACITY, "one C7 artifact exceeds page byte budget")
                    more = True
                    break
                items.append(json.loads(document)); size += amount; last = pos
            continuation = ArtifactCursor(workspace_id=self.profile.workspace_id, kind=kind, watermark=watermark, after=last) if more else None
            return ArtifactPage(items=tuple(items), next_cursor=continuation)
