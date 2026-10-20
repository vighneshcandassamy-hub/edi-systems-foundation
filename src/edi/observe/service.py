from contextlib import contextmanager
from threading import BoundedSemaphore
from typing import BinaryIO

from edi.observe.contracts import Capture, OriginSpec, ReplayCursor
from edi.observe.ports import ObservationStore
from edi.shared.config import LocalProfile
from edi.shared.contracts import Capability
from edi.shared.errors import EDIError, ErrorCode


class EvidenceAccess:
    """Downstream read facade. No capture, registry, checkpoint or SQL methods."""
    def __init__(self, service: "ObservationService", operations: frozenset[str]):
        self._service = service
        self._operations = operations

    def _allow(self, operation: str):
        if operation not in self._operations:
            raise EDIError(ErrorCode.DENIED, f"this reader lane does not permit {operation}")

    def get_origin(self, origin_ref: str):
        self._allow("select_records")
        return self._service.get_origin(origin_ref)

    def get_record(self, record_id: str):
        self._allow("select_records")
        return self._service.get_record(record_id)

    def replay(self, *, cursor: ReplayCursor | None = None,
               origin_ref: str | None = None, limit: int = 100):
        self._allow("select_records")
        return self._service.replay(cursor=cursor, origin_ref=origin_ref, limit=limit)

    def read_payload(self, record_id: str, *, offset: int = 0, length: int = 65536):
        self._allow("read_payload")
        return self._service.read_payload(record_id, offset=offset, length=length)

    def commit_status(self, origin_ref: str, idempotency_key: str):
        self._allow("commit_status")
        return self._service.commit_status(origin_ref, idempotency_key)

    def coverage(self):
        self._allow("coverage")
        return self._service.coverage()


class ObservationService:
    capability = Capability(
        owner="C1", functions=("F10", "F11", "F12", "F13"),
        state="implemented-unqualified",
        details="Native finite-stream intake, scoped origin continuity, atomic local commit, range reads/replay; partial F13",
    )

    def __init__(self, store: ObservationStore, profile: LocalProfile):
        self._store = store
        self._slots = BoundedSemaphore(profile.max_concurrent_operations)

    @contextmanager
    def _admit(self):
        if not self._slots.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "local operation slots exhausted", retryable=True)
        try:
            yield
        finally:
            self._slots.release()

    def reader(self, operations: frozenset[str]) -> EvidenceAccess:
        return EvidenceAccess(self, operations)

    def register_origin(self, spec: OriginSpec):
        with self._admit():
            return self._store.register_origin(spec)

    def ingest(self, capture: Capture, payload: BinaryIO):
        with self._admit():
            return self._store.ingest(capture, payload)

    def get_origin(self, origin_ref: str):
        with self._admit():
            return self._store.get_origin(origin_ref)

    def get_record(self, record_id: str):
        with self._admit():
            return self._store.get_record(record_id)

    def replay(self, *, cursor: ReplayCursor | None = None,
               origin_ref: str | None = None, limit: int = 100):
        with self._admit():
            return self._store.replay(cursor=cursor, origin_ref=origin_ref, limit=limit)

    def read_payload(self, record_id: str, *, offset: int = 0, length: int = 65536):
        with self._admit():
            return self._store.read_payload(record_id, offset=offset, length=length)

    def commit_status(self, origin_ref: str, idempotency_key: str):
        with self._admit():
            return self._store.commit_status(origin_ref, idempotency_key)

    def coverage(self):
        with self._admit():
            return self._store.coverage()

    def checkpoint(self, consumer_id: str, position: int):
        with self._admit():
            return self._store.checkpoint(consumer_id, position)

    def get_checkpoint(self, consumer_id: str):
        with self._admit():
            return self._store.get_checkpoint(consumer_id)

    def backup(self, destination):
        with self._admit():
            return self._store.backup(destination)
