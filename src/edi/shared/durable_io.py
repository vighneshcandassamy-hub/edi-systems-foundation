"""Bounded per-owner external-call journal. Never owns domain truth or credentials."""
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
from threading import RLock

from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


class CallJournal:
    """Use inside the declared owner's database; one synchronous writer per instance.

    Pending network work survives process restart. Network calls never hold SQL
    transactions. Physical WAL/disk bounds must also be set on the deployment.
    """
    def __init__(self, path, namespace, *, max_calls=512, max_bytes=64 * 1024**2):
        if not namespace.replace("_", "").isalnum():
            raise ValueError("invalid journal namespace")
        self.path, self.table = Path(path), "io_" + namespace
        self.max_calls, self.max_bytes = max_calls, max_bytes
        self.lock = RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute(f"CREATE TABLE IF NOT EXISTS {self.table}(id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, request TEXT NOT NULL, state TEXT NOT NULL, result TEXT, bytes INTEGER NOT NULL, attempts INTEGER NOT NULL)")

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA synchronous=FULL")
        try:
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def get(self, key):
        with self.connect() as db:
            row = db.execute(f"SELECT * FROM {self.table} WHERE id=?", (key,)).fetchone()
        return dict(row) if row else None

    def begin(self, key, body, *, reserve_bytes=1024 * 1024):
        encoded, fingerprint = canonical(body), digest(body)
        with self.lock, self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute(f"SELECT * FROM {self.table} WHERE id=?", (key,)).fetchone()
            if old:
                if old["fingerprint"] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "external request identity reused with changed input")
                return dict(old)
            count, size = db.execute(f"SELECT count(*),coalesce(sum(bytes),0) FROM {self.table}").fetchone()
            allowance = len(encoded.encode()) + reserve_bytes
            if count >= self.max_calls or size + allowance > self.max_bytes:
                raise EDIError(ErrorCode.CAPACITY, "external-call journal capacity exhausted")
            db.execute(f"INSERT INTO {self.table} VALUES (?,?,?,'pending',NULL,?,0)", (key, fingerprint, encoded, allowance))
        return self.get(key)

    def attempt(self, key):
        with self.connect() as db:
            db.execute(f"UPDATE {self.table} SET attempts=attempts+1 WHERE id=?", (key,))

    def claim_once(self, key):
        """Cross-process first-dispatch fence. No network retry is implied."""
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            cursor = db.execute(f"UPDATE {self.table} SET attempts=1 WHERE id=? AND attempts=0 AND state='pending'", (key,))
            return cursor.rowcount == 1

    def finish(self, key, result, *, state="completed"):
        encoded = canonical(result)
        with self.lock, self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute(f"SELECT * FROM {self.table} WHERE id=?", (key,)).fetchone()
            if not old:
                raise EDIError(ErrorCode.NOT_FOUND, "external intent is missing")
            if old["state"] != "pending":
                if old["result"] != encoded or old["state"] != state:
                    raise EDIError(ErrorCode.CONFLICT, "terminal external result cannot change")
                return
            if len(encoded.encode()) + len(old["request"].encode()) > old["bytes"]:
                raise EDIError(ErrorCode.CAPACITY, "external result exceeds prepaid allowance; reconcile pending work")
            db.execute(f"UPDATE {self.table} SET state=?,result=? WHERE id=?", (state, encoded, key))
