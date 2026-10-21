"""Actual EDI authority is separate from attributed world-actor information."""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.observe.contracts import Capture, Receipt, ReplayCursor
from edi.shared.contracts import EvidenceRef, Identifier, Record
from edi.world.contracts import Put, Ref, WorldCommit, WorldPatch

Text = Annotated[str, Field(min_length=1, max_length=8192)]
Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Operation = Literal["select-observations", "select-world"]


def aware(*times):
    if any(t is not None and t.utcoffset() is None for t in times):
        raise ValueError("C7 requires timezone-aware times")


class Grant(Record):
    grant_id: Identifier
    operation: Operation
    origin_refs: tuple[Identifier, ...] = Field(default=(), max_length=32)
    world_ids: tuple[Identifier, ...] = Field(default=(), max_length=32)
    not_before: datetime
    expires_at: datetime
    max_items: int = Field(default=25, ge=1, le=100)
    basis: Text

    @model_validator(mode="after")
    def scope(self):
        aware(self.not_before, self.expires_at)
        if self.expires_at <= self.not_before:
            raise ValueError("grant interval must be nonempty")
        if self.operation == "select-observations" and (not self.origin_refs or self.world_ids):
            raise ValueError("observation grants name exact origins only")
        if self.operation == "select-world" and (not self.world_ids or self.origin_refs):
            raise ValueError("world grants name exact record IDs only")
        if len(set(self.origin_refs)) != len(self.origin_refs) or len(set(self.world_ids)) != len(self.world_ids):
            raise ValueError("grant scope contains duplicate IDs")
        return self


class Policy(Record):
    policy_id: Identifier
    mode: Literal["research-readonly"] = "research-readonly"
    purpose_version: Identifier
    purpose: Text
    evaluation_standards: tuple[Text, ...] = Field(min_length=1, max_length=16)
    assumptions: tuple[Text, ...] = Field(min_length=1, max_length=16)
    grants: tuple[Grant, ...] = Field(default=(), max_length=32)
    decision_ttl_seconds: int = Field(default=60, ge=1, le=300)
    access_cooldown_seconds: int = Field(default=604800, ge=1, le=2592000)

    @model_validator(mode="after")
    def unique(self):
        if len({x.grant_id for x in self.grants}) != len(self.grants):
            raise ValueError("duplicate grant IDs")
        return self


class AmendmentRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    amendment_id: Identifier
    expected_revision: int = Field(ge=0)
    proposed: Policy
    change_kind: Literal["bootstrap", "parameter", "policy", "goal"]
    trigger: Text
    rationale: Text
    attribution: Text
    imported_advice: tuple[Identifier, ...] = Field(default=(), max_length=16)
    resource_and_implementation_basis: Text
    carry_over: Literal["retain-ledgers-recheck-unstarted-block-unresolved"] = "retain-ledgers-recheck-unstarted-block-unresolved"


class Amendment(Record):
    request: AmendmentRequest
    created_at: datetime
    profile_id: Identifier
    artifact_sha256: str
    status: Literal["proposed-not-adopted"] = "proposed-not-adopted"


class AdoptionRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    amendment_id: Identifier
    expected_revision: int = Field(ge=0)
    decision: Literal["adopt", "reject", "defer"]
    operator_id: Identifier
    rationale: Text


class Adoption(Record):
    request: AdoptionRequest
    amendment_sha256: Hash
    decided_at: datetime
    previous_revision: int = Field(ge=0)
    revision: int = Field(ge=0)
    policy: Policy | None
    authority: Literal["trusted-local-operator-unverified-identity"] = "trusted-local-operator-unverified-identity"
    artifact_sha256: str


class PolicyVersion(Record):
    workspace_id: Identifier
    revision: int = Field(ge=1)
    adoption: Adoption


class SelectObservations(Record):
    operation: Literal["select-observations"] = "select-observations"
    origin_ref: Identifier
    cursor: ReplayCursor | None = None
    limit: int = Field(default=25, ge=1, le=100)


class SelectWorld(Record):
    operation: Literal["select-world"] = "select-world"
    model_revision: int = Field(ge=1)
    refs: tuple[Ref, ...] = Field(min_length=1, max_length=32)

    @model_validator(mode="after")
    def pinned(self):
        if any(x.version is None for x in self.refs) or len({x.record_id for x in self.refs}) != len(self.refs):
            raise ValueError("world selections require unique pinned refs")
        return self


class UnsupportedAction(Record):
    operation: Literal["external-action", "acquire-source", "run-simulation"]
    description: Text


Intent = Annotated[SelectObservations | SelectWorld | UnsupportedAction, Field(discriminator="operation")]


class ActionRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    decision_id: Identifier
    policy_revision: int = Field(ge=1)
    purpose_version: Identifier
    grant_id: Identifier | None = None
    intent: Intent
    rationale: Text
    expected_effects_and_limits: Text
    attribution: Text
    boundary: Literal["edi-runtime"] = "edi-runtime"


class ActionDecision(Record):
    request: ActionRequest
    created_at: datetime
    expires_at: datetime
    policy_adoption_sha256: Hash
    status: Literal["allowed", "denied", "deferred"]
    reasons: tuple[Text, ...]
    artifact_sha256: str
    authority: Literal["research-policy-internal-read-only"] = "research-policy-internal-read-only"


class DispatchRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    execution_id: Identifier
    decision_id: Identifier


class ExecutionIntent(Record):
    request: DispatchRequest
    decision: ActionDecision
    created_at: datetime
    profile_id: Identifier
    artifact_sha256: str
    effect_class: Literal["internal-read-only"] = "internal-read-only"


class ExecutionReceipt(Record):
    execution_id: Identifier
    intent_sha256: Hash
    finished_at: datetime
    status: Literal["completed", "failed", "reported-completion", "reported-failure", "abandoned"]
    result: dict[str, JsonValue] | None = None
    report_archive_id: Identifier | None = None
    diagnostic: str | None = None
    reconciliation: dict[str, JsonValue] | None = None
    artifact_sha256: str
    measured_effect: Literal["not-established"] = "not-established"
    usage: dict[str, JsonValue] = Field(default_factory=lambda: {"model_calls": 0, "tokens": 0, "external_actions": 0, "end_to_end_cost": "unknown"})


class ExecutionStatus(Record):
    intent: ExecutionIntent
    receipt: ExecutionReceipt | None
    status: Literal["resolved", "completion-unresolved"]


class ReportRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    archive_id: Identifier
    execution_id: Identifier
    origin_ref: Identifier
    report_text: Annotated[str, Field(min_length=1, max_length=16384)]
    attribution: Text
    reported_at: datetime

    @model_validator(mode="after")
    def clock(self):
        aware(self.reported_at)
        return self


class ReportStage(Record):
    request: ReportRequest
    created_at: datetime
    capture: Capture


class ReportArchive(Record):
    stage: ReportStage
    receipt: Receipt
    artifact_sha256: str
    basis: Literal["local-operator-report-not-independent-effect"] = "local-operator-report-not-independent-effect"


class ReconcileRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    execution_id: Identifier
    archive_id: Identifier
    operator_id: Identifier
    outcome: Literal["reported-completion", "reported-failure", "abandoned"]
    rationale: Text


class AccessScope(Record):
    operation: Operation
    origin_refs: tuple[Identifier, ...] = Field(default=(), max_length=32)
    world_ids: tuple[Identifier, ...] = Field(default=(), max_length=32)
    max_items: int = Field(default=25, ge=1, le=100)

    @model_validator(mode="after")
    def scoped(self):
        if self.operation == "select-observations" and (not self.origin_refs or self.world_ids):
            raise ValueError("access scope requires exact origins")
        if self.operation == "select-world" and (not self.world_ids or self.origin_refs):
            raise ValueError("access scope requires exact world IDs")
        if len(set(self.origin_refs)) != len(self.origin_refs) or len(set(self.world_ids)) != len(self.world_ids):
            raise ValueError("duplicate access scope")
        return self


class AccessRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    access_id: Identifier
    scope: AccessScope
    target: Identifier
    unknown: Text
    hypothesis_family: Identifier
    minimum_useful_evidence: Text
    rationale: Text
    attribution: Text


class AccessReview(Record):
    request: AccessRequest
    created_at: datetime
    policy_revision: int = Field(ge=0)
    scope_key: Hash
    status: Literal["existing-grant", "needs-access", "coalesced", "denied-cooldown", "deferred"]
    grant_ids: tuple[Identifier, ...] = ()
    related_id: str | None = None
    review_after: datetime
    artifact_sha256: str
    notification: Literal["C0-owned-not-sent"] = "C0-owned-not-sent"


class AccessDispositionRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    disposition_id: Identifier
    access_id: Identifier
    operator_id: Identifier
    outcome: Literal["deny", "defer"]
    until: datetime
    rationale: Text

    @model_validator(mode="after")
    def clock(self):
        aware(self.until)
        return self


class AccessDisposition(Record):
    request: AccessDispositionRequest
    scope_key: Hash
    created_at: datetime
    artifact_sha256: str


class VisibleDatum(Record):
    datum_id: Identifier
    evidence: EvidenceRef | None = None
    model_ref: Ref | None = None
    available_at: datetime
    received_at: datetime | None = None
    perceived_at: datetime | None = None
    channel: Identifier
    content: JsonValue
    content_basis: Text
    uncertainty: Text

    @model_validator(mode="after")
    def causal_clock(self):
        aware(self.available_at, self.received_at, self.perceived_at)
        if (self.evidence is None) == (self.model_ref is None):
            raise ValueError("datum requires exactly one evidence or pinned model reference")
        if self.model_ref is not None and self.model_ref.version is None:
            raise ValueError("model datum requires pinned version")
        if self.received_at is not None and self.received_at < self.available_at:
            raise ValueError("receipt cannot precede availability")
        if self.perceived_at is not None and (self.received_at is None or self.perceived_at < self.received_at):
            raise ValueError("perception requires preceding receipt")
        return self


class ActorViewRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    view_id: Identifier
    actor: Ref
    model_revision: int = Field(ge=1)
    as_of: datetime
    clock_mapping_assumption: Text
    data: tuple[VisibleDatum, ...] = Field(default=(), max_length=32)
    owned_goals: tuple[Text, ...] = Field(default=(), max_length=16)
    frames_and_memory: tuple[Text, ...] = Field(default=(), max_length=16)
    attributed_policy: Text
    attribution: Text

    @model_validator(mode="after")
    def clock(self):
        aware(self.as_of)
        if self.actor.version is None or len({x.datum_id for x in self.data}) != len(self.data):
            raise ValueError("actor ref must be pinned and datum IDs unique")
        if any(t > self.as_of for x in self.data for t in (x.available_at, x.received_at, x.perceived_at) if t is not None):
            raise ValueError("actor datum includes future availability/receipt/perception")
        return self


class ActorView(Record):
    request: ActorViewRequest
    created_at: datetime
    basis: Literal["attributed-explicit-information-mask"] = "attributed-explicit-information-mask"
    limitations: tuple[Text, ...]
    artifact_sha256: str


class ModelUpdateRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    base_revision: int = Field(ge=0)
    operations: tuple[Put, ...] = Field(min_length=1, max_length=16)
    change_kind: Literal["policy", "organization", "explanation", "context"]
    rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    attribution: Text
    boundary: Literal["modeled-world"] = "modeled-world"
    basis: Literal["analyst-proposal"] = "analyst-proposal"

    @model_validator(mode="after")
    def candidate_only(self):
        if any(x.admission is not None for x in self.operations):
            raise ValueError("C7 cannot admit represented policies")
        if len({x.representation.record_id for x in self.operations}) != len(self.operations):
            raise ValueError("duplicate model targets")
        return self


class ModelStage(Record):
    request: ModelUpdateRequest
    patch: WorldPatch


class ModelSubmission(Record):
    request: ModelUpdateRequest
    commit: WorldCommit
    effect: Literal["candidate-model-update-not-domain-adoption"] = "candidate-model-update-not-domain-adoption"


class ArtifactCursor(Record):
    workspace_id: Identifier
    kind: Identifier
    watermark: int = Field(ge=0)
    after: int = Field(default=0, ge=0)


class ArtifactPage(Record):
    items: tuple[dict[str, JsonValue], ...]
    next_cursor: ArtifactCursor | None
