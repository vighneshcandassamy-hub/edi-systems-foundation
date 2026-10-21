"""C2-only immutable artifacts and submission receipts; no C1/C3 SQL access."""
from contextlib import contextmanager
import json
import shutil
import sqlite3

from edi.interpret.config import InterpretationProfile
from edi.interpret.contracts import Derivation, DerivationReceipt
from edi.shared.errors import EDIError, ErrorCode
from edi.world.contracts import WorldCommit, WorldPatch


def canonical(value):
    data = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SQLiteDerivationStore:
    def __init__(self, profile: InterpretationProfile):
        self.profile = profile
        self.path = profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C2 database")
                statements = [
                    "CREATE TABLE interpret_info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL, count INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0)",
                    "CREATE TABLE derivations (request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, derivation_id TEXT NOT NULL UNIQUE, document TEXT NOT NULL)",
                    "CREATE TABLE submissions (request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, patch TEXT NOT NULL, result TEXT)",
                ]
                for sql in statements:
                    con.execute(sql)
                con.execute("INSERT INTO interpret_info(singleton,workspace_id) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C2 schema version")
            scope = con.execute("SELECT workspace_id FROM interpret_info WHERE singleton=1").fetchone()
            if scope is None or scope[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C2 workspace mismatch")
            self._commit(con)

    @contextmanager
    def _connection(self):
        con = None
        try:
            con = sqlite3.connect(self.path, timeout=self.profile.writer_timeout_seconds, isolation_level=None)
            con.execute("PRAGMA synchronous=FULL")
            con.execute("PRAGMA cache_size=-8192")
            yield con
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.STORAGE, f"C2 storage unavailable: {exc}", retryable=True) from exc
        finally:
            if con is not None:
                try:
                    if con.in_transaction:
                        con.rollback()
                finally:
                    con.close()

    @staticmethod
    def _commit(con):
        try:
            con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C2 commit outcome unknown; query original request", retryable=True) from exc

    def find(self, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,document FROM derivations WHERE request_id=?", (request_id,)).fetchone()
            if row is None:
                return None
            if row[0] != fingerprint:
                raise EDIError(ErrorCode.CONFLICT, "C2 retry request/config differs")
            return Derivation.model_validate_json(row[1])

    def get(self, derivation_id):
        with self._connection() as con:
            row = con.execute("SELECT document FROM derivations WHERE derivation_id=?", (derivation_id,)).fetchone()
            if row is None:
                raise EDIError(ErrorCode.NOT_FOUND, "derivation unavailable")
            return Derivation.model_validate_json(row[0])

    def _reserve(self, con, size, *, derivation=False):
        count, used = con.execute("SELECT count,bytes FROM interpret_info WHERE singleton=1").fetchone()
        if (derivation and count >= self.profile.max_derivations) or used + size > self.profile.max_stored_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C2 artifact storage quota reached")
        if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C2 free disk reserve reached", retryable=True)

    def commit(self, fingerprint, derivation):
        encoded = canonical(derivation)
        size = len(encoded.encode("utf-8"))
        if size > self.profile.max_output_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C2 stored derivation exceeds output limit")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT fingerprint,document FROM derivations WHERE request_id=?",
                              (derivation.request.request_id,)).fetchone()
            if row is not None:
                if row[0] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "C2 concurrent retry conflict")
                return DerivationReceipt(derivation=Derivation.model_validate_json(row[1]), duplicate=True)
            self._reserve(con, size, derivation=True)
            con.execute("INSERT INTO derivations VALUES(?,?,?,?)",
                        (derivation.request.request_id, fingerprint, derivation.derivation_id, encoded))
            con.execute("UPDATE interpret_info SET count=count+1,bytes=bytes+? WHERE singleton=1", (size,))
            self._commit(con)
            return DerivationReceipt(derivation=derivation, duplicate=False)

    def submission(self, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,result FROM submissions WHERE request_id=?", (request_id,)).fetchone()
            if row is None:
                return None
            if row[0] != fingerprint:
                raise EDIError(ErrorCode.CONFLICT, "submission request differs")
            return WorldCommit.model_validate_json(row[1]) if row[1] is not None else None

    def submission_patch(self, request_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,patch FROM submissions WHERE request_id=?", (request_id,)).fetchone()
            if row is None:
                return None
            if row[0] != fingerprint:
                raise EDIError(ErrorCode.CONFLICT, "staged submission identity differs")
            return WorldPatch.model_validate_json(row[1])

    def prepare_submission(self, request_id, fingerprint, patch):
        encoded = canonical(patch)
        if len(encoded.encode("utf-8")) > self.profile.max_output_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C2 staged patch exceeds output profile")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT fingerprint,patch FROM submissions WHERE request_id=?", (request_id,)).fetchone()
            if row is not None:
                if row[0] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "staged submission conflict")
                return WorldPatch.model_validate_json(row[1])
            size = len(encoded.encode("utf-8"))
            self._reserve(con, size)
            if con.execute("SELECT COUNT(*) FROM submissions").fetchone()[0] >= self.profile.max_derivations:
                raise EDIError(ErrorCode.CAPACITY, "C2 staged submission count limit reached")
            con.execute("INSERT INTO submissions VALUES(?,?,?,NULL)", (request_id, fingerprint, encoded))
            con.execute("UPDATE interpret_info SET bytes=bytes+? WHERE singleton=1", (size,))
            self._commit(con)
            return WorldPatch.model_validate_json(encoded)

    def record_submission(self, request_id, fingerprint, result):
        encoded = canonical(result)
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = con.execute("SELECT fingerprint,result FROM submissions WHERE request_id=?", (request_id,)).fetchone()
            if previous is None or previous[0] != fingerprint:
                raise EDIError(ErrorCode.CONFLICT, "matching staged submission required for receipt")
            if previous[1] is not None:
                original = WorldCommit.model_validate_json(previous[1])
                if original.revision != result.revision or original.request_id != result.request_id:
                    raise EDIError(ErrorCode.INTEGRITY, "submission receipt changed its committed identity")
                return
            size = len(encoded.encode("utf-8"))
            self._reserve(con, size)
            con.execute("UPDATE submissions SET result=? WHERE request_id=?", (encoded, request_id))
            con.execute("UPDATE interpret_info SET bytes=bytes+? WHERE singleton=1", (size,))
            self._commit(con)
