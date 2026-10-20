"""C3 structural contracts, separate from executable C5 dynamics and C1 evidence."""
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field, JsonValue, model_validator

from edi.shared.contracts import EvidenceRef, Identifier, Owner, Quantity, Record


class Family(StrEnum):
    SYSTEM = "system-view"
    CONSTITUENT = "constituent"
    STOCK = "stock"
    FLOW = "flow-process"
    INFORMATION = "information-influence-link"
    RESPONSE = "response-relationship"
    PURPOSE = "function-purpose-reference-criterion"
    FEEDBACK = "feedback-path"
    HISTORY = "history-conditional-trajectory"


class Ref(Record):
    record_id: Identifier
    version: int | None = Field(default=None, ge=1)
    # None resolves to the post-patch target version on commit; stored references are pinned.


class Participant(Record):
    ref: Ref
    role: Identifier
    direction: Literal["in", "out", "in-out", "symmetric", "unknown"] = "unknown"
    port: str | None = None


class Validity(Record):
    status: Literal["unknown", "interval", "unbounded"] = "unknown"
    start: datetime | None = None
    end: datetime | None = None
    clock_id: Identifier = "UTC"

    @model_validator(mode="after")
    def consistent(self):
        for value in (self.start, self.end):
            if value is not None and value.utcoffset() is None:
                raise ValueError("valid-time bounds must be timezone aware")
        if self.status == "interval":
            if self.start is None and self.end is None:
                raise ValueError("interval requires at least one bound")
            if self.start is not None and self.end is not None and self.end <= self.start:
                raise ValueError("valid interval is [start,end) with end greater than start")
        elif self.start is not None or self.end is not None:
            raise ValueError("only interval validity has bounds")
        if self.clock_id != "UTC":
            raise ValueError("this profile supports UTC valid-time comparison only")
        return self


class SystemView(Record):
    family: Literal["system-view"] = "system-view"
    members: tuple[Ref, ...] = ()
    excluded: tuple[Ref, ...] = ()
    external_drivers: tuple[Ref, ...] = ()
    external_sinks: tuple[Ref, ...] = ()
    boundary: dict[str, JsonValue] = Field(default_factory=dict)
    purpose: str | None = None
    level: str | None = None
    resolution: dict[str, JsonValue] = Field(default_factory=dict)
    horizon: dict[str, JsonValue] = Field(default_factory=dict)
    closure_assumptions: tuple[str, ...] = ()


class Constituent(Record):
    family: Literal["constituent"] = "constituent"
    parts: tuple[Ref, ...] = ()
    roles: tuple[str, ...] = ()
    condition: dict[str, JsonValue] = Field(default_factory=dict)
    lifecycle: str = "unknown"


class Stock(Record):
    family: Literal["stock"] = "stock"
    quantity: Quantity
    inflows: tuple[Ref, ...] = ()
    outflows: tuple[Ref, ...] = ()
    initial_basis: str = "unknown"
    bounds: dict[str, JsonValue] = Field(default_factory=dict)
    reserve_and_access: dict[str, JsonValue] = Field(default_factory=dict)


class FlowProcess(Record):
    family: Literal["flow-process"] = "flow-process"
    participants: tuple[Participant, ...] = ()
    rate: Quantity | None = None
    response: Ref | None = None
    prerequisites: tuple[Ref, ...] = ()
    pending_commitments: tuple[Ref, ...] = ()
    transformation: dict[str, JsonValue] = Field(default_factory=dict)
    time_basis: str = "unknown"
    resource_use: dict[str, JsonValue] = Field(default_factory=dict)


class InformationLink(Record):
    family: Literal["information-influence-link"] = "information-influence-link"
    participants: tuple[Participant, ...] = ()
    channel: str | None = None
    meaning: dict[str, JsonValue] = Field(default_factory=dict)
    availability_receipt_attention: dict[str, JsonValue] = Field(default_factory=dict)
    distortion: dict[str, JsonValue] = Field(default_factory=dict)
    causal_status: Literal["unknown", "hypothesized", "reported"] = "unknown"


class ResponseRelationship(Record):
    family: Literal["response-relationship"] = "response-relationship"
    participants: tuple[Participant, ...] = ()
    mechanism: dict[str, JsonValue] = Field(default_factory=dict)
    parameters: dict[str, JsonValue] = Field(default_factory=dict)
    domains: dict[str, JsonValue] = Field(default_factory=dict)
    delays: dict[str, JsonValue] = Field(default_factory=dict)
    capacities: dict[str, JsonValue] = Field(default_factory=dict)
    execution_status: Literal["descriptive", "qualitative", "unsupported"] = "unsupported"


class PurposeCriterion(Record):
    family: Literal["function-purpose-reference-criterion"] = "function-purpose-reference-criterion"
    role: Literal["function", "purpose", "goal", "reference", "criterion", "constraint", "inquiry-objective"]
    owner: Ref | None = None
    attributed_basis: Literal["stated", "inferred", "assumed", "unknown"] = "unknown"
    definition: dict[str, JsonValue] = Field(default_factory=dict)
    horizon: dict[str, JsonValue] = Field(default_factory=dict)
    conflicts: tuple[Ref, ...] = ()
    feasibility: str = "unknown"
    normative_scope: str = "unknown"


class FeedbackPath(Record):
    family: Literal["feedback-path"] = "feedback-path"
    mechanisms: tuple[Ref, ...] = ()
    closure: Literal["unknown", "hypothesized", "reported"] = "unknown"
    polarity: Literal["unknown", "balancing", "reinforcing", "context-dependent"] = "unknown"
    delays: dict[str, JsonValue] = Field(default_factory=dict)
    applicability: dict[str, JsonValue] = Field(default_factory=dict)


class HistoryTrajectory(Record):
    family: Literal["history-conditional-trajectory"] = "history-conditional-trajectory"
    referents: tuple[Ref, ...] = ()
    origin: Literal["observation", "source-report", "forecast", "simulation", "unknown"] = "unknown"
    initial_history: tuple[Ref, ...] = ()
    points: tuple[dict[str, JsonValue], ...] = ()
    time_units_aggregation: dict[str, JsonValue] = Field(default_factory=dict)
    driver_assumptions: tuple[str, ...] = ()
    model_policy_versions: dict[str, JsonValue] = Field(default_factory=dict)
    run_id: str | None = None
    horizon: dict[str, JsonValue] = Field(default_factory=dict)


Structure = Annotated[
    SystemView | Constituent | Stock | FlowProcess | InformationLink | ResponseRelationship
    | PurposeCriterion | FeedbackPath | HistoryTrajectory, Field(discriminator="family")
]


class Representation(Record):
    record_id: Identifier
    scope_id: Identifier = "world"
    structure: Structure
    label: str | None = None
    dependencies: tuple[Ref, ...] = ()
    alternatives: tuple[Ref, ...] = ()
    alternative_group: str | None = None
    basis: Literal["source-report", "derivation", "assumption", "hypothesis", "imported", "unknown"] = "unknown"
    support: tuple[EvidenceRef, ...] = ()
    counterevidence: tuple[EvidenceRef, ...] = ()
    assumptions: tuple[str, ...] = ()
    uncertainty: dict[str, JsonValue] = Field(default_factory=lambda: {"status": "unknown"})
    validity: Validity = Field(default_factory=Validity)
    properties: dict[str, JsonValue] = Field(default_factory=dict)
    method_lineage: tuple[str, ...] = ()


def iter_refs(value):
    """Only typed Ref fields are dependencies. Opaque JSON is never interpreted as code/links."""
    if isinstance(value, Ref):
        yield value
    elif isinstance(value, BaseModel):
        for name in type(value).model_fields:
            yield from iter_refs(getattr(value, name))
    elif isinstance(value, (tuple, list)):
        for item in value:
            yield from iter_refs(item)


class Admission(Record):
    decision: Literal["candidate", "accepted_for_use", "rejected", "withdrawn"] = "candidate"
    rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    use_scope: str | None = None
    verification_obligation: str | None = None
    policy_id: Literal["local-modeling-use/1.0"] = "local-modeling-use/1.0"
    # No empirical-truth or independently-proven admission class is exposed.

    @model_validator(mode="after")
    def use(self):
        if self.decision == "accepted_for_use" and (not self.use_scope or not self.verification_obligation):
            raise ValueError("accepted_for_use requires scope and remaining verification obligation")
        return self


class Put(Record):
    operation: Literal["put"] = "put"
    representation: Representation
    expected_version: int = Field(ge=0)
    admission: Admission | None = None


class Decide(Record):
    operation: Literal["decide"] = "decide"
    record_id: Identifier
    expected_version: int = Field(ge=1)
    admission: Admission


class Retire(Record):
    operation: Literal["retire"] = "retire"
    record_id: Identifier
    expected_version: int = Field(ge=1)
    reason: Annotated[str, Field(min_length=1, max_length=4096)]


Operation = Annotated[Put | Decide | Retire, Field(discriminator="operation")]


class ConsumedEvidence(Record):
    consumer_id: Identifier
    expected_position: int = Field(ge=0)
    position: int = Field(ge=0)
    record_ids: tuple[str, ...]
    # C3 progress is committed with C3 state; C1 checkpoint remains a separate handoff.


class WorldPatch(Record):
    workspace_id: Identifier
    request_id: Identifier
    base_revision: int = Field(ge=0)
    proposer: Owner
    reason: Annotated[str, Field(min_length=1, max_length=4096)]
    change_kind: Literal["state", "parameter", "organization", "policy", "goal", "explanation", "context"]
    operations: tuple[Operation, ...] = Field(min_length=1)
    consumed: ConsumedEvidence | None = None


class StoredRepresentation(Record):
    workspace_id: Identifier
    version: int = Field(ge=1)
    known_at: datetime
    proposer: Owner
    change_kind: str
    representation: Representation
    state: Literal["candidate", "accepted_for_use", "rejected", "withdrawn", "retired"]
    admission: Admission
    decision_authority: Literal["C3-candidate-policy", "C3-local-operator"]
    use_validity: Literal["not-certified; inspect-dependencies-and-evidence"] = "not-certified; inspect-dependencies-and-evidence"


class WorldCommit(Record):
    workspace_id: Identifier
    request_id: Identifier
    revision: int = Field(ge=1)
    previous_revision: int = Field(ge=0)
    committed_at: datetime
    decision_authority: Literal["C3-candidate-policy", "C3-local-operator"]
    changed_ids: tuple[str, ...]
    invalidated_projection_ids: tuple[str, ...] = ("world.current",)
    dependency_impact: Literal["bounded-query-required"] = "bounded-query-required"
    # changed_ids is NOT an exhaustive transitive invalidation list.
    consumed: ConsumedEvidence | None = None
    duplicate: bool = False
    durability: Literal["local-sqlite-full-unqualified"] = "local-sqlite-full-unqualified"


class WorldQuery(Record):
    family: Family | None = None
    scope_id: str | None = None
    state: Literal["candidate", "accepted_for_use", "rejected", "withdrawn", "retired"] | None = None
    include_inactive: bool = False
    valid_at: datetime | None = None
    include_unknown_validity: bool = False

    @model_validator(mode="after")
    def time(self):
        if self.valid_at is not None and self.valid_at.utcoffset() is None:
            raise ValueError("valid_at requires timezone")
        return self


class WorldCursor(Record):
    workspace_id: Identifier
    revision: int = Field(ge=0)
    query: WorldQuery
    after_id: str = ""


class WorldPage(Record):
    workspace_id: Identifier
    revision: int = Field(ge=0)
    items: tuple[StoredRepresentation, ...]
    next_cursor: WorldCursor | None
    projection_status: Literal["revision-pinned"] = "revision-pinned"
    dependency_status: Literal["not-certified; query-dependencies-before-use"] = "not-certified; query-dependencies-before-use"


class DependencyItem(Record):
    owner_id: str
    owner_version: int
    target_id: str
    pinned_version: int
    visible_version: int | None
    visible_state: str | None
    validity: Literal["current", "changed", "inactive", "missing"]


class DependencyView(Record):
    revision: int
    root_id: str
    direction: Literal["dependencies", "dependents"]
    max_depth: int
    items: tuple[DependencyItem, ...]
    visited_ids: tuple[str, ...]
    complete: bool
    truncation: str | None
    depth_boundary_ids: tuple[str, ...] = ()
    # A depth boundary is explicitly incomplete, never an unbounded graph certificate.
