from pathlib import Path
from typing import BinaryIO
from threading import Lock

from edi.agency import Agency
from edi.analyze import Analysis
from edi.assess import Assessment
from edi.interpret import Interpretation
from edi.interpret.config import InterpretationProfile
from edi.interpret.sqlite import SQLiteDerivationStore
from edi.observe.contracts import Capture, OriginSpec
from edi.observe.service import ObservationService
from edi.observe.sqlite import SQLiteObservationStore
from edi.reason import Reasoning
from edi.shared.config import LocalProfile
from edi.shared.contracts import Capability, Owner
from edi.shared.errors import EDIError, ErrorCode
from edi.world import World
from edi.world.config import WorldProfile
from edi.world.sqlite import SQLiteWorldStore


class Runtime:
    """Local trusted SDK; not an authentication boundary or workflow engine."""
    def __init__(self, profile: LocalProfile, world_profile: WorldProfile | None = None,
                 interpretation_profile: InterpretationProfile | None = None):
        self.profile = profile
        world_profile = world_profile or WorldProfile(
            workspace_id=profile.workspace_id,
            database=profile.database.with_name(profile.database.stem + ".world.sqlite3"),
        )
        if world_profile.workspace_id != profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C1 and C3 workspace scopes must match")
        if world_profile.database.resolve() == profile.database.resolve():
            raise EDIError(ErrorCode.INVALID, "C1 and C3 require separate owner databases")
        interpretation_profile = interpretation_profile or InterpretationProfile(
            workspace_id=profile.workspace_id,
            database=profile.database.with_name(profile.database.stem + ".interpret.sqlite3"),
        )
        if interpretation_profile.workspace_id != profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C1/C2/C3 workspace scopes must match")
        paths = {profile.database.resolve(), world_profile.database.resolve(), interpretation_profile.database.resolve()}
        if len(paths) != 3:
            raise EDIError(ErrorCode.INVALID, "C1/C2/C3 require separate owner databases")
        self.observation = ObservationService(SQLiteObservationStore(profile), profile)
        self._world_profile = world_profile
        self._world = None
        self._world_lock = Lock()
        self._interpretation_profile = interpretation_profile
        self._interpretation = None
        self._interpretation_lock = Lock()
        self._components = {
            "C4": Reasoning(),
            "C5": Analysis(), "C6": Assessment(), "C7": Agency(),
        }

    def capabilities(self) -> tuple[Capability, ...]:
        return (
            Capability(owner="C0", functions=("F00", "F01", "F02", "F03"),
                       state="implemented-unqualified",
                       details="Partial C0: composition, scope/configuration, finite C1/C2/C3 operations and explicit progress handoff"),
            self.observation.capability,
            Interpretation.capability,
            World.capability,
            *(component.capability for component in self._components.values()),
        )

    @property
    def world(self) -> World:
        # C1 intake never waits for this lock or opens the C3 database.
        with self._world_lock:
            if self._world is None:
                self._world = World(SQLiteWorldStore(self._world_profile, self.reader_for("C3")),
                                    self._world_profile)
            return self._world

    @property
    def interpretation(self) -> Interpretation:
        # Decode/persist does not initialize C3; only submission requests its candidate port.
        with self._interpretation_lock:
            if self._interpretation is None:
                self._interpretation = Interpretation(
                    self._interpretation_profile, self.reader_for("C2"),
                    SQLiteDerivationStore(self._interpretation_profile), lambda: self.world_for("C2"),
                )
            return self._interpretation

    def reader_for(self, owner: Owner):
        lanes = {
            "C0": frozenset(("select_records", "commit_status", "coverage")),
            "C2": frozenset(("select_records", "read_payload", "coverage")),
            "C3": frozenset(("select_records", "commit_status")),
            "C4": frozenset(("select_records", "read_payload", "coverage")),
            "C5": frozenset(("select_records", "read_payload")),
            "C6": frozenset(("select_records", "read_payload", "coverage")),
            "C7": frozenset(("select_records",)),
        }
        if owner not in lanes:
            raise EDIError(ErrorCode.DENIED, "no downstream reader lane for this owner")
        # Deliberately read-only; C2/C3 use independently allocated operations.
        return self.observation.reader(lanes[owner])

    def register_origin(self, spec: OriginSpec):
        return self.observation.register_origin(spec)

    def observe(self, capture: Capture, stream: BinaryIO):
        return self.observation.ingest(capture, stream)

    def observe_file(self, capture: Capture, path: Path):
        # Opening is an explicitly supplied local path, never an implicit URL fetch.
        try:
            with path.open("rb") as stream:
                return self.observe(capture, stream)
        except OSError as exc:
            raise EDIError(ErrorCode.INCOMPLETE, "local input file unavailable") from exc

    def component(self, owner: Owner):
        component = self._components.get(owner)
        if component is None:
            raise EDIError(ErrorCode.INVALID, "use the C0/C1/C2/C3 typed SDK for this owner")
        return component

    def world_for(self, owner: Owner):
        return self.world.access_for(owner)

    def acknowledge_world_progress(self, consumer_id: str):
        # C3 durable progress comes first. No C3 -> C1 mutation lane is invented.
        position = self.world.consumer_position(consumer_id)
        return self.observation.checkpoint(consumer_id, position)
