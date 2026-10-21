from contextlib import contextmanager
from threading import BoundedSemaphore

from edi.shared.contracts import Capability, Owner
from edi.shared.errors import EDIError, ErrorCode
from edi.world.config import WorldProfile
from edi.world.contracts import WorldPatch
from edi.world.ports import WorldStore


class WorldAccess:
    """Owner-scoped read/proposal interface; no administrative admission or database handle."""
    def __init__(self, service: "World", owner: Owner, operations: frozenset[str]):
        self._service, self._owner, self._operations = service, owner, operations

    def _allow(self, operation):
        if operation not in self._operations:
            raise EDIError(ErrorCode.DENIED, f"{self._owner} has no C3 {operation} operation")

    def get(self, record_id, *, revision=None):
        self._allow("read_view")
        return self._service.get(record_id, revision=revision)

    def query(self, query=None, *, revision=None, cursor=None, limit=100):
        self._allow("read_view")
        return self._service.query(query, revision=revision, cursor=cursor, limit=limit)

    def propose_patch(self, patch: WorldPatch):
        self._allow("propose_patch")
        if patch.proposer != self._owner:
            raise EDIError(ErrorCode.DENIED, "proposal owner differs from allocated port")
        return self._service.propose_patch(patch)

    def dependencies(self, record_id, *, revision=None, direction="dependencies", max_depth=1):
        self._allow("dependencies")
        return self._service.dependencies(record_id, revision=revision,
                                          direction=direction, max_depth=max_depth)

    def commit_status(self, request_id):
        self._allow("commit_status")
        return self._service.commit_status(request_id)

    def actor_view(self, *args, **kwargs):
        raise EDIError(ErrorCode.UNAVAILABLE,
                       "actor perception/visibility policy is not installed; a global snapshot is not an actor view")


class World:
    capability = Capability(
        owner="C3", functions=("F30", "F31", "F32", "F33"), state="implemented-unqualified",
        details="Partial C3: nine-family hosting, candidate/operator admission, append-only revisions, bounded views/dependencies and revision-invalidated SQL projections",
    )

    def __init__(self, store: WorldStore, profile: WorldProfile):
        self._store = store
        self._slots = BoundedSemaphore(profile.max_concurrent_operations)

    @contextmanager
    def _admit(self):
        if not self._slots.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "world operation slots exhausted", retryable=True)
        try:
            yield
        finally:
            self._slots.release()

    def access_for(self, owner: Owner):
        lanes = {
            "C0": frozenset(("read_view", "propose_patch", "dependencies", "commit_status")),
            "C2": frozenset(("propose_patch", "dependencies", "commit_status")),
            "C4": frozenset(("read_view", "propose_patch", "dependencies", "commit_status")),
            "C5": frozenset(("read_view", "dependencies")),
            "C6": frozenset(("read_view", "propose_patch", "dependencies", "commit_status")),
            "C7": frozenset(("read_view", "propose_patch", "dependencies", "commit_status")),
        }
        if owner not in lanes:
            raise EDIError(ErrorCode.DENIED, "no model read/proposal lane for this owner")
        return WorldAccess(self, owner, lanes[owner])

    def propose_patch(self, patch: WorldPatch):
        with self._admit():
            return self._store.commit(patch, allow_decisions=False)

    def commit(self, patch: WorldPatch):
        """Trusted local operator only; deliberately absent from WorldAccess."""
        with self._admit():
            return self._store.commit(patch, allow_decisions=True)

    def head(self):
        with self._admit():
            return self._store.head()

    def get(self, record_id, *, revision=None):
        with self._admit():
            return self._store.get(record_id, revision=revision)

    def query(self, query=None, *, revision=None, cursor=None, limit=100):
        with self._admit():
            return self._store.query(query, revision=revision, cursor=cursor, limit=limit)

    def dependencies(self, record_id, *, revision=None, direction="dependencies", max_depth=1):
        with self._admit():
            return self._store.dependencies(record_id, revision=revision,
                                            direction=direction, max_depth=max_depth)

    def commit_status(self, request_id):
        with self._admit():
            return self._store.commit_status(request_id)

    def consumer_position(self, consumer_id):
        with self._admit():
            return self._store.consumer_position(consumer_id)
