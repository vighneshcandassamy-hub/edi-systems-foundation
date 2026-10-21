"""C6-only immutable artifacts, bounded selection and prepaid seal confirmations."""
from contextlib import contextmanager
import json
import shutil
import sqlite3

from edi.assess.contracts import ArtifactCursor, ArtifactPage
from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    value = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SQLiteAssessmentStore:
    def __init__(self, profile):
        self.profile, self.path = profile, profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C6 database")
                con.execute("CREATE TABLE assessment_info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL, records INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0)")
                con.execute("CREATE TABLE artifacts (position INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, artifact_id TEXT NOT NULL, request_id TEXT NOT NULL, fingerprint TEXT NOT NULL, document TEXT NOT NULL, UNIQUE(kind,artifact_id), UNIQUE(kind,request_id))")
                con.execute("CREATE INDEX artifact_selection ON artifacts(kind,position)")
                con.execute("INSERT INTO assessment_info(singleton,workspace_id) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C6 schema")
            scope = con.execute("SELECT workspace_id FROM assessment_info WHERE singleton=1").fetchone()
            if scope is None or scope[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C6 store workspace differs")
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
            raise EDIError(ErrorCode.STORAGE, f"C6 storage unavailable: {exc}", retryable=True) from exc
        finally:
            if con is not None:
                try:
                    if con.in_transaction: con.rollback()
                finally: con.close()

    @staticmethod
    def _commit(con):
        try: con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C6 commit outcome unknown; query original artifact/request", retryable=True) from exc

    def find(self, kind, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,document FROM artifacts WHERE kind=? AND request_id=?", (kind, request_id)).fetchone()
            if row is None: return None
            if row[0] != fingerprint: raise EDIError(ErrorCode.CONFLICT, "C6 original request/semantics changed")
            return json.loads(row[1])

    def get(self, kind, artifact_id):
        with self._connection() as con:
            row = con.execute("SELECT document FROM artifacts WHERE kind=? AND artifact_id=?", (kind, artifact_id)).fetchone()
            if row is None: raise EDIError(ErrorCode.NOT_FOUND, f"C6 {kind} artifact unavailable")
            return json.loads(row[0])

    def optional(self, kind, artifact_id):
        try: return self.get(kind, artifact_id)
        except EDIError as exc:
            if exc.code == ErrorCode.NOT_FOUND: return None
            raise

    def put(self, kind, artifact_id, request_id, fingerprint, document):
        encoded = canonical(document)
        size = len(encoded.encode("utf-8"))
        if size > self.profile.max_document_bytes: raise EDIError(ErrorCode.CAPACITY, "C6 document byte limit exceeded")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = con.execute("SELECT request_id,fingerprint,document FROM artifacts WHERE kind=? AND (artifact_id=? OR request_id=?)", (kind, artifact_id, request_id)).fetchall()
            if previous:
                if len(previous) != 1 or previous[0][0] != request_id or previous[0][1] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "C6 artifact/request identity conflict")
                return json.loads(previous[0][2])
            if kind in ("confirmation", "receipt"):
                parent, allowance = ("forecast", 16384) if kind == "confirmation" else ("stage", 32768)
                if size > allowance or con.execute("SELECT artifact_id FROM artifacts WHERE kind=? AND artifact_id=?", (parent, artifact_id)).fetchone() is None:
                    raise EDIError(ErrorCode.INVALID, "C6 confirmation requires its prepaid durable forecast")
                # A forecast already reserved one confirmation row and 16 KiB.
            else:
                extra_count, extra_bytes = (2, 16384) if kind == "forecast" else (2, 32768) if kind == "stage" else (1, 0)
                count, used = con.execute("SELECT records,bytes FROM assessment_info WHERE singleton=1").fetchone()
                if count + extra_count > self.profile.max_records or used + size + extra_bytes > self.profile.max_stored_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C6 retained-artifact quota reached")
                if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C6 disk reserve reached", retryable=True)
                con.execute("UPDATE assessment_info SET records=records+?,bytes=bytes+? WHERE singleton=1", (extra_count, size + extra_bytes))
            con.execute("INSERT INTO artifacts(kind,artifact_id,request_id,fingerprint,document) VALUES(?,?,?,?,?)", (kind, artifact_id, request_id, fingerprint, encoded))
            self._commit(con)
            return json.loads(encoded)

    def query(self, kind="comparison", *, cursor=None, limit=25):
        if kind not in ("comparison", "review", "finding", "yield") or type(limit) is not int or not 1 <= limit <= 100:
            raise EDIError(ErrorCode.INVALID, "invalid C6 artifact selection")
        if cursor is not None and (cursor.kind != kind or cursor.workspace_id != self.profile.workspace_id or cursor.after > cursor.watermark):
            raise EDIError(ErrorCode.DENIED, "C6 cursor selection/scope differs")
        with self._connection() as con:
            con.execute("BEGIN")
            high = con.execute("SELECT COALESCE(MAX(position),0) FROM artifacts").fetchone()[0]
            watermark, after = (high, 0) if cursor is None else (cursor.watermark, cursor.after)
            if watermark > high: raise EDIError(ErrorCode.INVALID, "C6 cursor exceeds store history")
            rows = con.execute("SELECT position,document FROM artifacts WHERE kind=? AND position>? AND position<=? ORDER BY position LIMIT ?", (kind, after, watermark, limit + 1))
            items, size, last, more = [], 0, after, False
            for pos, document in rows:
                amount = len(document.encode("utf-8"))
                if len(items) >= limit or size + amount > self.profile.max_page_bytes:
                    if not items: raise EDIError(ErrorCode.CAPACITY, "one C6 artifact exceeds this page byte profile")
                    more = True
                    break
                items.append(json.loads(document)); size += amount; last = pos
            next_cursor = ArtifactCursor(kind=kind, watermark=watermark, after=last, workspace_id=self.profile.workspace_id) if more else None
            return ArtifactPage(items=tuple(items), next_cursor=next_cursor)
