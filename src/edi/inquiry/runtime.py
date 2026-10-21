from pathlib import Path
from typing import BinaryIO
from threading import Lock

from edi.agency import Agency
from edi.analyze import Analysis
from edi.analyze.config import AnalysisProfile
from edi.analyze.sqlite import SQLiteAnalysisStore
from edi.assess import Assessment
from edi.assess.config import AssessmentProfile
from edi.assess.sqlite import SQLiteAssessmentStore
from edi.interpret import Interpretation
from edi.interpret.config import InterpretationProfile
from edi.interpret.sqlite import SQLiteDerivationStore
from edi.observe.contracts import Capture, OriginSpec
from edi.observe.service import ObservationService
from edi.observe.sqlite import SQLiteObservationStore
from edi.reason import Reasoning
from edi.reason.config import ReasoningProfile
from edi.reason.sqlite import SQLiteReasoningStore
from edi.shared.config import LocalProfile
from edi.shared.contracts import Capability, Owner
from edi.shared.errors import EDIError, ErrorCode
from edi.world import World
from edi.world.config import WorldProfile
from edi.world.sqlite import SQLiteWorldStore


class Runtime:
    """Local trusted SDK; not an authentication boundary or workflow engine."""
    def __init__(self, profile: LocalProfile, world_profile: WorldProfile | None = None,
                 interpretation_profile: InterpretationProfile | None = None,
                 reasoning_profile: ReasoningProfile | None = None,
                 analysis_profile: AnalysisProfile | None = None,
                 assessment_profile: AssessmentProfile | None = None):
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
        reasoning_profile = reasoning_profile or ReasoningProfile(
            workspace_id=profile.workspace_id,
            database=profile.database.with_name(profile.database.stem + ".reason.sqlite3"),
        )
        if reasoning_profile.workspace_id != profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C1/C2/C3/C4 workspace scopes must match")
        if reasoning_profile.database.resolve() in paths:
            raise EDIError(ErrorCode.INVALID, "C1/C2/C3/C4 require separate owner databases")
        analysis_profile = analysis_profile or AnalysisProfile(
            workspace_id=profile.workspace_id,
            database=profile.database.with_name(profile.database.stem + ".analyze.sqlite3"),
        )
        if analysis_profile.workspace_id != profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C1-C5 workspace scopes must match")
        if analysis_profile.database.resolve() in paths | {reasoning_profile.database.resolve()}:
            raise EDIError(ErrorCode.INVALID, "C1-C5 require separate owner databases")
        assessment_profile = assessment_profile or AssessmentProfile(
            workspace_id=profile.workspace_id,
            database=profile.database.with_name(profile.database.stem + ".assess.sqlite3"),
        )
        if assessment_profile.workspace_id != profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C1-C6 workspace scopes must match")
        if assessment_profile.database.resolve() in paths | {reasoning_profile.database.resolve(), analysis_profile.database.resolve()}:
            raise EDIError(ErrorCode.INVALID, "C1-C6 require separate owner databases")
        self.observation = ObservationService(SQLiteObservationStore(profile), profile)
        self._world_profile = world_profile
        self._world = None
        self._world_lock = Lock()
        self._interpretation_profile = interpretation_profile
        self._interpretation = None
        self._interpretation_lock = Lock()
        self._reasoning_profile = reasoning_profile
        self._reasoning = None
        self._reasoning_lock = Lock()
        self._analysis_profile = analysis_profile
        self._analysis = None
        self._analysis_lock = Lock()
        self._assessment_profile = assessment_profile
        self._assessment = None
        self._assessment_lock = Lock()
        self._components = {
            "C7": Agency(),
        }

    def capabilities(self) -> tuple[Capability, ...]:
        return (
            Capability(owner="C0", functions=("F00", "F01", "F02", "F03"),
                       state="implemented-unqualified",
                       details="Partial C0: composition, scope/configuration, finite C1-C6 operations and explicit progress handoff; no autonomous scheduling"),
            self.observation.capability,
            Interpretation.capability,
            World.capability,
            Reasoning.capability,
            Analysis.capability,
            Assessment.capability,
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

    @property
    def reasoning(self) -> Reasoning:
        # C1 intake opens neither C4 nor C3; C4 opens C3 only when its port is used.
        with self._reasoning_lock:
            if self._reasoning is None:
                self._reasoning = Reasoning(
                    self._reasoning_profile, self.reader_for("C4"),
                    SQLiteReasoningStore(self._reasoning_profile), lambda: self.world_for("C4"),
                    lambda: self.assessment_for("C4"),
                )
            return self._reasoning

    def register_origin(self, spec: OriginSpec):
        return self.observation.register_origin(spec)

    @property
    def analysis(self) -> Analysis:
        with self._analysis_lock:
            if self._analysis is None:
                self._analysis = Analysis(
                    self._analysis_profile, self.reader_for("C5"),
                    SQLiteAnalysisStore(self._analysis_profile), lambda: self.world_for("C5"),
                    lambda: self.assessment_for("C5"),
                )
            return self._analysis

    def analysis_for(self, owner: Owner):
        if owner != "C6":
            raise EDIError(ErrorCode.DENIED, "no C5 component port is allocated to this owner")
        return self.analysis.access_for(owner)

    @property
    def assessment(self) -> Assessment:
        with self._assessment_lock:
            if self._assessment is None:
                self._assessment = Assessment(
                    self._assessment_profile, self.reader_for("C6"),
                    SQLiteAssessmentStore(self._assessment_profile), lambda: self.world_for("C6"),
                    lambda: self.analysis_for("C6"),
                )
            return self._assessment

    def assessment_for(self, owner: Owner):
        if owner not in ("C4", "C5"):
            raise EDIError(ErrorCode.DENIED, "no C6 component port allocated for this owner")
        return self.assessment.access_for(owner)

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
            raise EDIError(ErrorCode.INVALID, "use the C0-C6 typed SDK for this owner")
        return component

    def world_for(self, owner: Owner):
        return self.world.access_for(owner)

    def acknowledge_world_progress(self, consumer_id: str):
        # C3 durable progress comes first. No C3 -> C1 mutation lane is invented.
        position = self.world.consumer_position(consumer_id)
        return self.observation.checkpoint(consumer_id, position)
