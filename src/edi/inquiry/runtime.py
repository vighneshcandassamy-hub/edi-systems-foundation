from pathlib import Path
from typing import BinaryIO

from edi.agency import Agency
from edi.analyze import Analysis
from edi.assess import Assessment
from edi.interpret import Interpretation
from edi.observe.contracts import Capture, OriginSpec
from edi.observe.service import ObservationService
from edi.observe.sqlite import SQLiteObservationStore
from edi.reason import Reasoning
from edi.shared.config import LocalProfile
from edi.shared.contracts import Capability, Owner
from edi.shared.errors import EDIError, ErrorCode
from edi.world import World


class Runtime:
    """Local trusted SDK; not an authentication boundary or workflow engine."""
    def __init__(self, profile: LocalProfile):
        self.profile = profile
        self.observation = ObservationService(SQLiteObservationStore(profile), profile)
        self._components = {
            "C2": Interpretation(), "C3": World(), "C4": Reasoning(),
            "C5": Analysis(), "C6": Assessment(), "C7": Agency(),
        }

    def capabilities(self) -> tuple[Capability, ...]:
        return (
            Capability(owner="C0", functions=("F00", "F01", "F02", "F03"),
                       state="implemented-unqualified",
                       details="Partial C0: composition, explicit scope/configuration and finite C1 operations only"),
            self.observation.capability,
            *(component.capability for component in self._components.values()),
        )

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
        # Deliberately read-only; C2-C7 implementations are still unavailable.
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
            raise EDIError(ErrorCode.INVALID, "use the C0/C1 typed SDK for this owner")
        return component
