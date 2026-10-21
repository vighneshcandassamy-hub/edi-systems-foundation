from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

Identifier = Annotated[str, Field(min_length=1, max_length=256)]
Owner = Literal["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid4())


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True, allow_inf_nan=False)
    schema_version: Literal["1.0"] = "1.0"


class TimeValue(Record):
    status: Literal["known", "unknown"] = "unknown"
    value: datetime | None = None
    reason: str | None = "not supplied"

    @model_validator(mode="after")
    def consistent(self):
        if self.status == "known":
            if self.value is None or self.value.utcoffset() is None:
                raise ValueError("known time requires a timezone-aware datetime")
            if self.reason is not None:
                raise ValueError("known time must not have an unknown reason")
        elif self.value is not None or not self.reason:
            raise ValueError("unknown time requires a reason and no value")
        return self


class TemporalScope(Record):
    event_time: TimeValue = Field(default_factory=TimeValue)
    reported_time: TimeValue = Field(default_factory=TimeValue)
    clock_id: str | None = None
    sequence: int | None = Field(default=None, ge=0)
    # Source-declared gaps/uncertainty belong in a profile, never inferred from silence.


class EvidenceRef(Record):
    workspace_id: Identifier
    record_id: Identifier
    sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    selector: str = "whole-object"
    origin_class: Literal["external", "generated", "simulation", "unknown"] = "unknown"
    lineage: tuple[str, ...] = ()


class RecordIdentity(Record):
    workspace_id: Identifier
    record_id: Identifier
    kind: Identifier
    immutable_revision: Identifier


class Quantity(Record):
    """Exact numeric strings are retained; conversion is an explicit later derivation."""
    status: Literal["known", "unknown", "missing", "not-applicable"]
    value: str | int | float | bool | None = None
    scale: Literal["cardinal", "ordinal", "categorical", "unknown"] = "unknown"
    unit: str | None = None
    unknown_reason: str | None = None
    context: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def consistent(self):
        if self.status == "known" and self.value is None:
            raise ValueError("known quantity requires a value")
        if self.status != "known" and (self.value is not None or not self.unknown_reason):
            raise ValueError("unavailable quantity requires a reason and no fabricated value")
        return self


class Assertion(Record):
    workspace_id: Identifier
    claim_id: Identifier
    participants: tuple[str, ...]
    predicate: Identifier
    descriptive_roles: tuple[str, ...]
    basis: Literal["source-report", "derivation", "assumption", "hypothesis"]
    support: tuple[EvidenceRef, ...] = ()
    counterevidence: tuple[EvidenceRef, ...] = ()
    applicability: dict[str, JsonValue] = Field(default_factory=dict)
    state: Literal["candidate", "withdrawn", "superseded"] = "candidate"
    # This proposal contract cannot issue C3's future accepted-for-use decision.


class CommandEnvelope(Record):
    workspace_id: Identifier
    request_id: Identifier
    operation: Identifier
    producer: Owner
    profile_id: Identifier
    body: dict[str, JsonValue]
    idempotency_key: Identifier | None = None
    base_revision: str | None = None
    deadline: datetime | None = None


class ResultEnvelope(Record):
    request_id: Identifier
    producer: Owner
    status: Literal["committed", "available", "unavailable", "rejected", "partial"]
    body_or_reference: dict[str, JsonValue]


class ModelPatch(Record):
    """Proposal only. Construction does not grant C3 admission authority."""
    workspace_id: Identifier
    proposal_id: Identifier
    base_revision: Identifier
    proposer: Owner
    operations: tuple[dict[str, JsonValue], ...]
    reason: str
    evidence: tuple[EvidenceRef, ...] = ()
    assumptions: tuple[str, ...] = ()


class ModelDelta(Record):
    workspace_id: Identifier
    previous_revision: Identifier
    revision: Identifier
    affected_ids: tuple[str, ...]
    invalidated_projection_ids: tuple[str, ...] = ()


class RefinementBridge(Record):
    workspace_id: Identifier
    bridge_id: Identifier
    coarse_ref: Identifier
    fine_refs: tuple[str, ...]
    mapping_ref: Identifier
    applicability: dict[str, JsonValue]


class KnowledgeRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    direction: Literal["outward", "inward", "temporal"]
    question: str
    target_refs: tuple[str, ...]
    discriminates: tuple[str, ...]
    requested_access: tuple[str, ...] = ()
    # A request never constitutes an access grant.


class ExplorationFrontier(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    model_revision: Identifier
    pending: tuple[KnowledgeRequest, ...] = ()


class Capability(Record):
    owner: Owner
    functions: tuple[str, ...]
    state: Literal["implemented-unqualified", "declared-unavailable"]
    details: str
