"""C4-owned bounded journal and current episode projection; no cross-owner SQL."""
from contextlib import contextmanager
import json
import shutil
import sqlite3

from edi.reason.config import ReasoningProfile
from edi.reason.contracts import Episode
from edi.shared.errors import EDIError, ErrorCode


def canonical(value):
    data = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SQLiteReasoningStore:
    def __init__(self, profile: ReasoningProfile):
        self.profile = profile
        self.path = profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized C4 database")
                for sql in (
                    "CREATE TABLE reason_info (singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL, episodes INTEGER NOT NULL DEFAULT 0, commands INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0)",
                    "CREATE TABLE episodes (inquiry_id TEXT PRIMARY KEY, sequence INTEGER NOT NULL, active INTEGER NOT NULL, document TEXT NOT NULL)",
                    "CREATE UNIQUE INDEX one_unresolved_job ON episodes(active) WHERE active=1",
                    "CREATE TABLE commands (command_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, inquiry_id TEXT NOT NULL, sequence INTEGER NOT NULL, document TEXT NOT NULL)",
                    "CREATE INDEX command_history ON commands(inquiry_id,sequence)",
                ):
                    con.execute(sql)
                con.execute("INSERT INTO reason_info(singleton,workspace_id) VALUES(1,?)", (profile.workspace_id,))
                con.execute("PRAGMA user_version=1")
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported C4 schema")
            scope = con.execute("SELECT workspace_id FROM reason_info WHERE singleton=1").fetchone()
            if scope is None or scope[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "C4 workspace mismatch")
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
            raise EDIError(ErrorCode.STORAGE, f"C4 storage unavailable: {exc}", retryable=True) from exc
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
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "C4 commit outcome unknown; query original command", retryable=True) from exc

    def find(self, command_id, fingerprint):
        with self._connection() as con:
            row = con.execute("SELECT fingerprint,document FROM commands WHERE command_id=?", (command_id,)).fetchone()
            if row is None:
                return None
            if row[0] != fingerprint:
                raise EDIError(ErrorCode.CONFLICT, "C4 command identity/request/profile differs")
            return Episode.model_validate_json(row[1])

    def get(self, inquiry_id, *, sequence=None):
        with self._connection() as con:
            row = (con.execute("SELECT document FROM episodes WHERE inquiry_id=?", (inquiry_id,)).fetchone()
                   if sequence is None else con.execute("SELECT document FROM commands WHERE inquiry_id=? AND sequence=?", (inquiry_id, sequence)).fetchone())
            if row is None:
                raise EDIError(ErrorCode.NOT_FOUND, "C4 inquiry unavailable")
            return Episode.model_validate_json(row[0])

    def status(self, command_id):
        with self._connection() as con:
            row = con.execute("SELECT document FROM commands WHERE command_id=?", (command_id,)).fetchone()
            return Episode.model_validate_json(row[0]) if row is not None else None

    def save(self, command_id, fingerprint, episode, *, expected_sequence):
        encoded = canonical(episode)
        size = len(encoded.encode("utf-8"))
        if size > self.profile.max_episode_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C4 episode size limit reached")
        # Journal + current projection are both charged conservatively; never reclaimed silently.
        charge = 2 * size
        active = int(any(job.status == "awaiting-import" for job in episode.jobs))
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            original = con.execute("SELECT fingerprint,document FROM commands WHERE command_id=?", (command_id,)).fetchone()
            if original is not None:
                if original[0] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "concurrent C4 command conflict")
                return Episode.model_validate_json(original[1])
            current = con.execute("SELECT sequence FROM episodes WHERE inquiry_id=?", (episode.request.inquiry_id,)).fetchone()
            previous = current[0] if current else 0
            if previous != expected_sequence or episode.sequence != previous + 1:
                raise EDIError(ErrorCode.CONFLICT, "C4 sequence changed; inspect current inquiry", retryable=True)
            if active and con.execute("SELECT inquiry_id FROM episodes WHERE active=1 AND inquiry_id<>?", (episode.request.inquiry_id,)).fetchone():
                raise EDIError(ErrorCode.CAPACITY, "one unresolved C4 model job per workspace", retryable=True)
            count, commands, used = con.execute("SELECT episodes,commands,bytes FROM reason_info WHERE singleton=1").fetchone()
            if ((current is None and count >= self.profile.max_episodes) or commands >= self.profile.max_commands
                    or used + charge > self.profile.max_stored_bytes):
                raise EDIError(ErrorCode.CAPACITY, "C4 storage quota reached")
            if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
                raise EDIError(ErrorCode.CAPACITY, "C4 free disk reserve reached", retryable=True)
            con.execute("INSERT INTO commands VALUES(?,?,?,?,?)", (command_id, fingerprint, episode.request.inquiry_id, episode.sequence, encoded))
            con.execute("INSERT INTO episodes VALUES(?,?,?,?) ON CONFLICT(inquiry_id) DO UPDATE SET sequence=excluded.sequence,active=excluded.active,document=excluded.document",
                        (episode.request.inquiry_id, episode.sequence, active, encoded))
            con.execute("UPDATE reason_info SET episodes=episodes+?,commands=commands+1,bytes=bytes+? WHERE singleton=1", (int(current is None), charge))
            self._commit(con)
            return Episode.model_validate_json(encoded)
