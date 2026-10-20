"""Finite, single-host C1 adapter with one payload/metadata transaction boundary.

No network input, decoding, inferred subject identity, retention eviction or HA.
Use trusted, finite, blocking binary files/streams; deadlines are cooperative.
"""
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sqlite3
from time import monotonic
from typing import BinaryIO

from edi.observe.contracts import (
    Capture, CommitStatus, Manifest, Observation, Origin, OriginSpec,
    Receipt, ReplayCursor, ReplayPage,
)
from edi.shared.config import LocalProfile
from edi.shared.contracts import new_id, utc_now
from edi.shared.errors import EDIError, ErrorCode

_SCHEMA = """
CREATE TABLE store_info (
    singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL,
    record_count INTEGER NOT NULL DEFAULT 0, payload_bytes INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE sources (
    source_id TEXT PRIMARY KEY, namespace TEXT NOT NULL, native_id TEXT NOT NULL,
    UNIQUE(namespace,native_id)
);
CREATE TABLE origins (
    origin_ref TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(source_id),
    epoch TEXT NOT NULL, spec_json TEXT NOT NULL, record_json TEXT NOT NULL,
    UNIQUE(source_id,epoch)
);
CREATE TABLE observations (
    position INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL UNIQUE,
    origin_ref TEXT NOT NULL REFERENCES origins(origin_ref), idem_key TEXT NOT NULL,
    fingerprint TEXT NOT NULL, record_json TEXT NOT NULL,
    UNIQUE(origin_ref,idem_key)
);
CREATE INDEX observations_origin_position ON observations(origin_ref,position);
CREATE TABLE payload_chunks (
    record_id TEXT NOT NULL REFERENCES observations(record_id) DEFERRABLE INITIALLY DEFERRED,
    ordinal INTEGER NOT NULL, start_byte INTEGER NOT NULL, byte_count INTEGER NOT NULL,
    digest TEXT NOT NULL, payload BLOB NOT NULL, PRIMARY KEY(record_id,ordinal)
);
CREATE INDEX payload_ranges ON payload_chunks(record_id,start_byte);
CREATE TABLE checkpoints (
    consumer_id TEXT PRIMARY KEY, position INTEGER NOT NULL
);
PRAGMA user_version=1;
"""


def _canonical(record) -> str:
    return json.dumps(record.model_dump(mode="json"), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False, allow_nan=False)


class SQLiteObservationStore:
    def __init__(self, profile: LocalProfile):
        self.profile = profile
        self.path = profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                tables = con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
                if tables:
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized database; no migration applied")
                # execute statements individually: executescript would implicitly commit.
                for statement in _SCHEMA.split(";"):
                    if statement.strip():
                        con.execute(statement)
                con.execute("INSERT INTO store_info(singleton,workspace_id) VALUES(1,?)",
                            (profile.workspace_id,))
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, f"unsupported store schema {version}")
            workspace = con.execute("SELECT workspace_id FROM store_info WHERE singleton=1").fetchone()
            if workspace is None or workspace[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "database belongs to a different workspace")
            self._commit(con)

    @contextmanager
    def _connection(self):
        con = None
        try:
            con = sqlite3.connect(self.path, timeout=self.profile.writer_timeout_seconds,
                                  isolation_level=None)
            con.execute("PRAGMA foreign_keys=ON")
            con.execute("PRAGMA synchronous=FULL")
            con.execute("PRAGMA cache_size=-8192")
            yield con
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.STORAGE, f"SQLite operation failed: {exc}",
                           retryable=True) from exc
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
            raise EDIError(ErrorCode.UNKNOWN_COMMIT,
                           "commit acknowledgement failed; resolve by idempotency status",
                           retryable=True) from exc

    def _metadata(self, record) -> str:
        value = _canonical(record)
        if len(value.encode("utf-8")) > self.profile.max_metadata_bytes:
            raise EDIError(ErrorCode.CAPACITY, "metadata exceeds configured byte limit")
        return value

    def _disk_capacity(self):
        if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
            raise EDIError(ErrorCode.CAPACITY, "free disk reserve reached", retryable=True)

    def register_origin(self, spec: OriginSpec) -> Origin:
        spec_json = self._metadata(spec)
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            source = con.execute("SELECT source_id FROM sources WHERE namespace=? AND native_id=?",
                                 (spec.namespace, spec.native_source_id)).fetchone()
            source_id = source[0] if source else new_id()
            existing = con.execute("SELECT spec_json,record_json FROM origins WHERE source_id=? AND epoch=?",
                                   (source_id, spec.epoch)).fetchone()
            if existing:
                if existing[0] != spec_json:
                    raise EDIError(ErrorCode.CONFLICT,
                                   "origin descriptor is immutable; register a new epoch for change")
                return Origin.model_validate_json(existing[1])
            if con.execute("SELECT COUNT(*) FROM origins").fetchone()[0] >= self.profile.max_origins:
                raise EDIError(ErrorCode.CAPACITY, "origin registry limit reached")
            self._disk_capacity()
            origin = Origin(workspace_id=self.profile.workspace_id, source_id=source_id,
                            origin_ref=new_id(), registered_at=utc_now(), spec=spec)
            if not source:
                con.execute("INSERT INTO sources VALUES(?,?,?)",
                            (source_id, spec.namespace, spec.native_source_id))
            con.execute("INSERT INTO origins VALUES(?,?,?,?,?)",
                        (origin.origin_ref, source_id, spec.epoch, spec_json, self._metadata(origin)))
            self._commit(con)
            return origin

    def _origin(self, con, origin_ref: str) -> Origin:
        row = con.execute("SELECT record_json FROM origins WHERE origin_ref=?", (origin_ref,)).fetchone()
        if row is None:
            raise EDIError(ErrorCode.NOT_FOUND, "origin is not registered in this workspace")
        return Origin.model_validate_json(row[0])

    def get_origin(self, origin_ref: str) -> Origin:
        with self._connection() as con:
            return self._origin(con, origin_ref)

    def ingest(self, capture: Capture, payload: BinaryIO) -> Receipt:
        capture_json = self._metadata(capture)
        if capture.expected_bytes is not None and capture.expected_bytes > self.profile.max_record_bytes:
            raise EDIError(ErrorCode.CAPACITY, "declared record exceeds configured byte limit")
        record_id, receipt_time = new_id(), utc_now()
        started = monotonic()
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            origin = self._origin(con, capture.origin_ref)
            previous = con.execute(
                "SELECT fingerprint,record_json FROM observations WHERE origin_ref=? AND idem_key=?",
                (capture.origin_ref, capture.idempotency_key),
            ).fetchone()
            count, used = con.execute(
                "SELECT record_count,payload_bytes FROM store_info WHERE singleton=1"
            ).fetchone()
            if previous is None and count >= self.profile.max_records:
                raise EDIError(ErrorCode.CAPACITY, "record count limit reached")
            digest, total, ordinal = sha256(), 0, 0
            while True:
                if monotonic() - started > self.profile.max_ingest_seconds:
                    raise EDIError(ErrorCode.CAPACITY, "cooperative ingest deadline exceeded")
                try:
                    chunk = payload.read(self.profile.max_chunk_bytes)
                except OSError as exc:
                    raise EDIError(ErrorCode.INCOMPLETE, "payload input could not be read") from exc
                if not isinstance(chunk, bytes) or len(chunk) > self.profile.max_chunk_bytes:
                    raise EDIError(ErrorCode.INVALID, "input must honor bounded binary read(size)")
                if not chunk:
                    break
                total += len(chunk)
                if total > self.profile.max_record_bytes or ordinal >= self.profile.max_chunks_per_record:
                    raise EDIError(ErrorCode.CAPACITY, "record byte/chunk limit reached")
                if previous is None:
                    if used + total > self.profile.max_payload_bytes:
                        raise EDIError(ErrorCode.CAPACITY, "retained payload quota reached")
                    self._disk_capacity()
                    con.execute("INSERT INTO payload_chunks VALUES(?,?,?,?,?,?)",
                                (record_id, ordinal, total - len(chunk), len(chunk),
                                 sha256(chunk).hexdigest(), chunk))
                digest.update(chunk)
                ordinal += 1
            if monotonic() - started > self.profile.max_ingest_seconds:
                raise EDIError(ErrorCode.CAPACITY, "cooperative ingest deadline exceeded")
            if capture.expected_bytes is not None and capture.expected_bytes != total:
                raise EDIError(ErrorCode.INCOMPLETE, "acquired length differs from expected length")
            payload_hash = digest.hexdigest()
            if capture.expected_sha256 is not None and capture.expected_sha256 != payload_hash:
                raise EDIError(ErrorCode.INTEGRITY, "acquired payload hash differs from expected hash")
            fingerprint = sha256((capture_json + "\n" + payload_hash).encode("utf-8")).hexdigest()
            if previous:
                if previous[0] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "retry key reused with different metadata or bytes")
                return Receipt(observation=Observation.model_validate_json(previous[1]), duplicate=True)
            cursor = con.execute(
                "INSERT INTO observations(record_id,origin_ref,idem_key,fingerprint,record_json) VALUES(?,?,?,?,?)",
                (record_id, capture.origin_ref, capture.idempotency_key, fingerprint, ""),
            )
            position = cursor.lastrowid
            if position is None:
                raise EDIError(ErrorCode.STORAGE, "database did not assign a commit position")
            observation = Observation(
                record_id=record_id, scope_id=self.profile.workspace_id, kind=capture.kind,
                receipt_time=receipt_time, origin_ref=origin.origin_ref, manifest_ref=record_id + ":manifest",
                profiles=capture.profiles, committed_at=utc_now(), commit_position=position,
                source_id=origin.source_id, capture=capture,
                manifest=Manifest(sha256=payload_hash, byte_count=total, chunk_count=ordinal,
                                  chunk_bytes=self.profile.max_chunk_bytes, media_type=capture.media_type),
            )
            con.execute("UPDATE observations SET record_json=? WHERE record_id=?",
                        (self._metadata(observation), record_id))
            con.execute("UPDATE store_info SET record_count=record_count+1,payload_bytes=payload_bytes+? WHERE singleton=1",
                        (total,))
            self._commit(con)
            return Receipt(observation=observation, duplicate=False)

    def get_record(self, record_id: str) -> Observation:
        with self._connection() as con:
            row = con.execute("SELECT record_json FROM observations WHERE record_id=?", (record_id,)).fetchone()
            if row is None:
                raise EDIError(ErrorCode.NOT_FOUND, "observation unavailable")
            return Observation.model_validate_json(row[0])

    def commit_status(self, origin_ref: str, idempotency_key: str) -> CommitStatus:
        with self._connection() as con:
            self._origin(con, origin_ref)
            row = con.execute("SELECT record_id,position FROM observations WHERE origin_ref=? AND idem_key=?",
                              (origin_ref, idempotency_key)).fetchone()
            if row is None:
                return CommitStatus(status="not-found")
            return CommitStatus(status="committed", record_id=row[0], commit_position=row[1])

    def replay(self, *, cursor: ReplayCursor | None = None,
               origin_ref: str | None = None, limit: int = 100) -> ReplayPage:
        if type(limit) is not int or not 1 <= limit <= self.profile.max_page_records:
            raise EDIError(ErrorCode.CAPACITY, "replay page limit outside configured bounds")
        with self._connection() as con:
            con.execute("BEGIN")
            high = con.execute("SELECT COALESCE(MAX(position),0) FROM observations").fetchone()[0]
            if cursor is None:
                cursor = ReplayCursor(workspace_id=self.profile.workspace_id,
                                      watermark=high, origin_ref=origin_ref)
            elif cursor.workspace_id != self.profile.workspace_id or cursor.watermark > high:
                raise EDIError(ErrorCode.INVALID, "cursor does not belong to available history")
            elif origin_ref is not None and origin_ref != cursor.origin_ref:
                raise EDIError(ErrorCode.INVALID, "cursor filter cannot change during replay")
            if cursor.origin_ref is not None:
                self._origin(con, cursor.origin_ref)
            query = "SELECT record_json FROM observations WHERE position>? AND position<=?"
            params = [cursor.after, cursor.watermark]
            if cursor.origin_ref is not None:
                query += " AND origin_ref=?"
                params.append(cursor.origin_ref)
            query += " ORDER BY position LIMIT ?"
            params.append(limit + 1)
            rows = con.execute(query, params).fetchall()
            items = tuple(Observation.model_validate_json(row[0]) for row in rows[:limit])
            has_more = len(rows) > limit
            after = items[-1].commit_position if has_more else cursor.watermark
            next_cursor = ReplayCursor(workspace_id=cursor.workspace_id, after=after,
                                       watermark=cursor.watermark, origin_ref=cursor.origin_ref)
            return ReplayPage(items=items, cursor=next_cursor, has_more=has_more)

    def read_payload(self, record_id: str, *, offset: int = 0, length: int = 65536) -> bytes:
        if type(offset) is not int or type(length) is not int or offset < 0 or not 0 <= length <= self.profile.max_read_bytes:
            raise EDIError(ErrorCode.CAPACITY, "payload range outside configured bounds")
        record = self.get_record(record_id)
        total = record.manifest.byte_count
        if offset > total:
            raise EDIError(ErrorCode.INVALID, "offset exceeds payload length")
        end = min(offset + length, total)
        if end == offset:
            return b""
        parts = []
        with self._connection() as con:
            rows = con.execute(
                "SELECT start_byte,byte_count,digest,payload FROM payload_chunks "
                "WHERE record_id=? AND start_byte<? AND start_byte+byte_count>? ORDER BY ordinal",
                (record_id, end, offset),
            )
            for start, size, digest, data in rows:
                if len(data) != size or sha256(data).hexdigest() != digest:
                    raise EDIError(ErrorCode.INTEGRITY, "stored payload chunk failed verification")
                parts.append(data[max(0, offset-start):min(size, end-start)])
        result = b"".join(parts)
        if len(result) != end - offset:
            raise EDIError(ErrorCode.INTEGRITY, "stored payload range is incomplete")
        return result

    def get_checkpoint(self, consumer_id: str) -> int:
        if not consumer_id or len(consumer_id) > 256:
            raise EDIError(ErrorCode.INVALID, "invalid consumer identity")
        with self._connection() as con:
            row = con.execute("SELECT position FROM checkpoints WHERE consumer_id=?", (consumer_id,)).fetchone()
            return row[0] if row else 0

    def checkpoint(self, consumer_id: str, position: int) -> int:
        if not consumer_id or len(consumer_id) > 256 or type(position) is not int or position < 0:
            raise EDIError(ErrorCode.INVALID, "invalid consumer checkpoint")
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            high = con.execute("SELECT COALESCE(MAX(position),0) FROM observations").fetchone()[0]
            previous = con.execute("SELECT position FROM checkpoints WHERE consumer_id=?", (consumer_id,)).fetchone()
            if position > high or (previous and position < previous[0]):
                raise EDIError(ErrorCode.CONFLICT, "checkpoint must be monotonic and within committed history")
            if not previous and con.execute("SELECT COUNT(*) FROM checkpoints").fetchone()[0] >= self.profile.max_consumers:
                raise EDIError(ErrorCode.CAPACITY, "consumer registry limit reached")
            con.execute("INSERT INTO checkpoints VALUES(?,?) ON CONFLICT(consumer_id) DO UPDATE SET position=excluded.position",
                        (consumer_id, position))
            self._commit(con)
            return position

    def coverage(self) -> dict:
        with self._connection() as con:
            con.execute("BEGIN")
            count, size = con.execute("SELECT record_count,payload_bytes FROM store_info WHERE singleton=1").fetchone()
            high = con.execute("SELECT COALESCE(MAX(position),0) FROM observations").fetchone()[0]
            origins = con.execute("SELECT COUNT(*) FROM origins").fetchone()[0]
        return {"workspace_id": self.profile.workspace_id, "records": count,
                "payload_bytes": size, "origins": origins, "watermark": high,
                "source_loss": "unknown; only supplied gap profiles are recorded",
                "retention": "retain until explicit future policy; quota rejection, no eviction",
                "durability": "local-sqlite-full-unqualified", "ha": False,
                "mandatory_model_calls": 0}

    def backup(self, destination: Path) -> None:
        """Exclusive new destination; SQLite backup includes payloads and all C1 state."""
        destination = destination.resolve()
        if destination == self.path:
            raise EDIError(ErrorCode.INVALID, "backup destination equals active database")
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with destination.open("xb"):
                pass
        except FileExistsError as exc:
            raise EDIError(ErrorCode.CONFLICT, "backup destination already exists") from exc
        try:
            with self._connection() as source:
                target = sqlite3.connect(destination)
                try:
                    target.execute("PRAGMA synchronous=FULL")
                    started = monotonic()

                    def progress(status, remaining, total):
                        if monotonic() - started > self.profile.max_backup_seconds:
                            raise EDIError(ErrorCode.CAPACITY,
                                           "backup deadline exceeded; destination may be incomplete")
                        if shutil.disk_usage(destination.parent).free < self.profile.min_free_disk_bytes:
                            raise EDIError(ErrorCode.CAPACITY,
                                           "backup disk reserve reached; destination may be incomplete")

                    source.backup(target, pages=256, sleep=0.01, progress=progress)
                finally:
                    target.close()
        except (sqlite3.Error, OSError) as exc:
            raise EDIError(ErrorCode.STORAGE, "backup failed; destination may be incomplete") from exc
