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


class AgencyObservationAccess(EvidenceAccess):
    """IF-13B: exact C7-generated reports only; no general intake/registry handle."""
    def __init__(self, service):
        super().__init__(service, frozenset(("select_records",)))

    def ingest_report(self, capture: Capture, payload: BinaryIO):
        if (capture.kind != "execution-report" or capture.origin_class != "generated"
                or not capture.lineage or capture.lineage[0] != "edi-c7/0.8.0"
                or capture.media_type != "text/plain; charset=utf-8"
                or capture.expected_bytes is None or capture.expected_bytes > 65536
                or capture.expected_sha256 is None):
            raise EDIError(ErrorCode.DENIED, "C7 report facade accepts only bounded attributed generated reports")
        origin = self._service.get_origin(capture.origin_ref)
        spec = origin.spec
        if (spec.namespace != "edi.agency.reports" or spec.adapter != "edi-c7-report/1.0"
                or spec.deliverer != "C0-local-operator" or spec.binding_basis != "configured"):
            raise EDIError(ErrorCode.DENIED, "C7 cannot report through an unrelated origin")
        return self._service.ingest(capture, payload)


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

    def agency_access(self):
        return AgencyObservationAccess(self)

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
