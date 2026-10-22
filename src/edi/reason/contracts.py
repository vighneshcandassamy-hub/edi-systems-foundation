"""Bounded, attributed reasoning artifacts; none constitute causal proof or access grants."""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.observe.contracts import Origin
from edi.shared.contracts import EvidenceRef, Identifier, Record, TemporalScope
from edi.world.contracts import DependencyView, Put, StoredRepresentation, WorldCommit, WorldPatch

Text = Annotated[str, Field(min_length=1, max_length=8192)]
Axis = Literal["evidence", "boundary", "organization", "accumulation", "feedback-delay",
               "nonlinearity", "agency", "resilience-evolution", "rivals", "intervention", "learning"]
Direction = Literal["expand_adjacent", "refine_internal", "resolve_identity", "refresh_temporal",
                    "test_mechanism", "check_boundary", "review_abstraction"]
Trigger = Literal["unexplained_prediction_error", "contradictory_source", "uncertain_high_impact_interface",
                  "near_threshold", "aging_assumption", "insufficient_resolution",
                  "decision_sensitive_unknown", "bounded_periodic_review"]


class ModelBinding(Record):
    model_id: Identifier = "unbound"
    revision: Identifier = "unbound"
    provider: Identifier = "unbound"
    engine: Identifier = "unbound"
    tokenizer_revision: Identifier = "unknown"
    weights: Literal["fixed"] = "fixed"


class Budget(Record):
    rounds: int = Field(default=2, ge=1, le=4)
    rivals_per_round: int = Field(default=3, ge=1, le=3)
    jobs: int = Field(default=4, ge=1, le=6)
    reserved_tokens: int = Field(default=32768, ge=1, le=131072)
    input_token_cap: int = Field(default=4096, ge=1, le=16384)
    output_token_cap: int = Field(default=4096, ge=1, le=16384)


class EvidenceSelection(Record):
    record_id: Identifier
    offset: int = Field(default=0, ge=0)
    length: int = Field(default=4096, ge=0, le=65536)


class AssessmentNote(Record):
    """C0 imports an attributed C6 record; C4 does not manufacture C6's verdict."""
    assessment_id: Identifier
    source_revision: Identifier
    summary: Text
    status: Literal["imported-unverified"] = "imported-unverified"


class InquiryRequest(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    question: Text
    purpose: Text
    scope: Text
    horizon: Text
    model_revision: int = Field(ge=0)
    world_ids: tuple[Identifier, ...] = Field(default=(), max_length=16)
    evidence: tuple[EvidenceSelection, ...] = Field(default=(), max_length=16)
    axes: tuple[Axis, ...] = Field(default=("evidence", "boundary", "rivals", "learning"), min_length=1, max_length=11)
    omitted_frontier: tuple[Text, ...] = Field(default=(), max_length=32)
    unknowns: tuple[Text, ...] = Field(default=(), max_length=32)
    assessments: tuple[AssessmentNote, ...] = Field(default=(), max_length=8)
    budget: Budget = Field(default_factory=Budget)

    @model_validator(mode="after")
    def unique(self):
        if len(set(self.axes)) != len(self.axes) or len(set(self.world_ids)) != len(self.world_ids):
            raise ValueError("duplicate context IDs or protocol axes")
        return self


class EvidenceSlice(Record):
    reference: EvidenceRef
    origin: Origin
    receipt_time: datetime
    committed_at: datetime
    time: TemporalScope
    completeness: Literal["complete", "partial", "unknown"]
    critical_profiles: tuple[str, ...] = ()
    media_type: str
    selected_bytes: int = Field(ge=0)
    excerpt: str | None = None
    interpretation: Literal["utf8-untrusted-source-content", "metadata-only"]
    limitation: str | None = None


class Context(Record):
    model_revision: int
    world: tuple[StoredRepresentation, ...]
    dependencies: tuple[DependencyView, ...]
    evidence: tuple[EvidenceSlice, ...]
    limitations: tuple[str, ...]
    sha256: str
    # Hash identifies the complete bounded cut, never completeness of the real world.


class ProtocolQuestion(Record):
    axis: Axis
    question: Text


class Job(Record):
    job_id: Identifier
    role: Literal["student", "teacher"]
    round: int = Field(ge=1, le=4)
    binding: ModelBinding
    context_sha256: str
    protocol_id: Identifier
    questions: tuple[ProtocolQuestion, ...]
    input_token_cap: int
    output_token_cap: int
    created_at: datetime
    reason: Text
    teacher_trigger: Literal["novel", "unresolved", "consequential", "student-escalation"] | None = None
    status: Literal["awaiting-import", "completed", "cancelled-usage-unknown", "rejected"] = "awaiting-import"
    response_id: str | None = None
    dispatch: Literal["export-only; no model call performed"] = "export-only; no model call performed"


class Prediction(Record):
    conditions: Text
    expected_observation: Text
    rival_difference: Text
    channel: Text
    horizon: Text


class Hypothesis(Record):
    hypothesis_id: Identifier
    claim: Text
    mechanism: Text
    scope: Text
    support: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    counterevidence: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    dependence_groups: tuple[Text, ...] = Field(default=(), max_length=16)
    assumptions: tuple[Text, ...] = Field(default=(), max_length=16)
    confounders: tuple[Text, ...] = Field(default=(), max_length=16)
    applicability: Text
    unknowns: tuple[Text, ...] = Field(min_length=1, max_length=16)
    predictions: tuple[Prediction, ...] = Field(default=(), max_length=8)
    rivals: tuple[Identifier, ...] = Field(default=(), max_length=8)
    status: Literal["candidate"] = "candidate"


class InquiryTest(Record):
    test_id: Identifier
    discriminates: tuple[Identifier, ...] = Field(min_length=1, max_length=6)
    intervention_or_observation: Text
    expected_differences: Text
    channels: tuple[Text, ...] = Field(min_length=1, max_length=8)
    feasibility: Text
    confounding_controls: Text
    cost_and_risk: Text
    identifiability_limit: Text
    kind: Literal["observation", "qualitative-analysis", "numerical-analysis"]
    status: Literal["proposed-unrun"] = "proposed-unrun"


class FrontierItem(Record):
    frontier_id: Identifier
    direction: Direction
    trigger: Trigger
    target: Text
    unknown: Text
    hypothesis_family: Identifier
    capability_scope: tuple[Identifier, ...] = Field(default=(), max_length=16)
    relevance: float = Field(ge=0, le=1)
    discrimination: float = Field(ge=0, le=1)
    impact: float = Field(ge=0, le=1)
    feasibility: float = Field(ge=0, le=1)
    relative_cost: float = Field(ge=0, le=1)
    rationale: Text
    state: Literal["open", "deferred", "denied", "resolved"] = "open"
    disposition_reason: Text = "awaiting C0 scheduling/access review"
    material_change: str | None = None
    # Scores are declared judgments, not probabilities, posteriors or measured EIG.


class CandidateChange(Record):
    hypothesis_id: Identifier
    put: Put


class OperationProposal(Record):
    """Data-only request to C0; never a grant, operator input or execution receipt."""
    operation: Literal["world-call", "acquire-asset", "select-context", "analysis-compile", "analysis-run", "teacher-review", "component-call", "yield"]
    arguments: dict[str, JsonValue]

    @model_validator(mode="after")
    def native_argument_shape(self):
        from edi.reason.operation_args import validate_arguments
        validate_arguments(self.operation, self.arguments)
        return self


class Response(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    response_id: Identifier
    job_id: Identifier
    context_sha256: str
    origin: Literal["human-authored", "external-model-output"]
    attribution: Text
    binding: ModelBinding
    rationale_summary: Text
    hypotheses: tuple[Hypothesis, ...] = Field(default=(), max_length=3)
    tests: tuple[InquiryTest, ...] = Field(default=(), max_length=8)
    frontier: tuple[FrontierItem, ...] = Field(default=(), max_length=16)
    candidates: tuple[CandidateChange, ...] = Field(default=(), max_length=16)
    operation_proposals: tuple[OperationProposal, ...] = Field(default=(), max_length=1)
    feedback_disposition: Literal["not-applicable", "retained-for-review", "challenged", "deferred"] = "not-applicable"
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    limitation: Text


class StepRequest(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    action: Literal["student", "teacher", "yield", "cancel-pending"]
    reason: Text
    teacher_trigger: Literal["novel", "unresolved", "consequential", "student-escalation"] | None = None


class FrontierUpdate(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    item: FrontierItem


class OutboxAck(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    message_ids: tuple[Identifier, ...] = Field(min_length=1, max_length=256)
    disposition: Text
    # C0 local receipt only; not proof of execution, acquired evidence or a grant.


class SubmissionRequest(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    response_id: Identifier
    reason: Text


class Submission(Record):
    request: SubmissionRequest
    patch: WorldPatch
    receipt: WorldCommit | None = None


class OutboxItem(Record):
    message_id: Identifier
    kind: Literal["candidate_patch", "test_spec", "exploration_frontier", "knowledge_request_proposal", "deferred_frontier"]
    artifact_id: Identifier
    artifact_sequence: int = Field(ge=1)
    recipient: Literal["C0"] = "C0"
    status: Literal["pending", "acknowledged"] = "pending"
    acknowledgement: str | None = None


class RejectedResponse(Record):
    workspace_id: Identifier
    inquiry_id: Identifier
    request_id: Identifier
    job_id: Identifier
    raw_record_id: Identifier
    context_sha256: str
    diagnostic: Text
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    status: Literal["returned-output-rejected"] = "returned-output-rejected"


class Episode(Record):
    request: InquiryRequest
    sequence: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    implementation: Literal["edi-c4/0.6.0"] = "edi-c4/0.6.0"
    profile_snapshot: dict[str, JsonValue]
    operating_profile: dict[str, JsonValue]
    context: Context
    jobs: tuple[Job, ...] = ()
    responses: tuple[Response, ...] = ()
    rejections: tuple[RejectedResponse, ...] = ()
    frontier: tuple[FrontierItem, ...] = ()
    outbox: tuple[OutboxItem, ...] = ()
    submissions: tuple[Submission, ...] = ()
    tokens_reserved: int = Field(default=0, ge=0)
    state: Literal["ready", "awaiting-response", "round-complete", "yielded"] = "ready"
    stop_reason: str | None = None
    qualification: Literal["source-only; runtime unqualified"] = "source-only; runtime unqualified"
