"""C6 prospective registration, correspondence, assessment and advice records."""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.analyze.contracts import Program, RunRequest, Unit
from edi.observe.contracts import Origin
from edi.shared.contracts import EvidenceRef, Identifier, Record
from edi.world.contracts import DependencyView, Put, Ref, WorldCommit, WorldPatch

Text = Annotated[str, Field(min_length=1, max_length=8192)]
Scalar = Annotated[float, Field(allow_inf_nan=False)]
Cause = Literal["observation-error", "semantic-misalignment", "numerical-error", "unexpected-drivers",
                "wrong-parameters", "wrong-rule-or-topology", "changed-policy", "non-identifiability"]


class ForecastCase(Record):
    case_id: Identifier
    stock_symbol: Identifier
    relative_time: Scalar
    origin_ref: Identifier
    variable: Identifier
    declared_dependence_group: Identifier
    interpretation: Literal["point", "bernoulli-probability"]
    score_limit: float = Field(ge=0)
    interpretation_basis: Text


class EvaluationRule(Record):
    selection_policy: Literal["first-matching-measurement-by-commit"] = "first-matching-measurement-by-commit"
    aggregation: Literal["instantaneous-state"] = "instantaneous-state"
    require_disjoint_sources: bool = True
    source_independence_assumption: Text
    calibration_edges: tuple[Scalar, ...] = (0.0, 0.25, 0.5, 0.75, 1.0)
    missing_policy: Literal["retain-denominator; no-imputation"] = "retain-denominator; no-imputation"
    censored_policy: Literal["report-unscored"] = "report-unscored"

    @model_validator(mode="after")
    def bins(self):
        if not 2 <= len(self.calibration_edges) <= 21 or self.calibration_edges[0] != 0 or self.calibration_edges[-1] != 1:
            raise ValueError("calibration bins must cover [0,1] with at most twenty bins")
        if any(b <= a for a, b in zip(self.calibration_edges, self.calibration_edges[1:])):
            raise ValueError("calibration bin edges must be strictly ordered")
        return self


class SealRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    forecast_id: Identifier
    run_id: Identifier
    variant: Identifier = "baseline"
    cases: tuple[ForecastCase, ...] = Field(min_length=1, max_length=128)
    rule: EvaluationRule
    assumptions: tuple[Text, ...] = Field(min_length=1, max_length=32)
    rationale: Text


class SealedPoint(Record):
    case: ForecastCase
    target_time: datetime
    predicted: Scalar
    unit: Unit
    world_ref: Ref


class ForecastSeal(Record):
    request: SealRequest
    prepared_at: datetime
    c1_watermark: int = Field(ge=0)
    run_sha256: str
    compiled_sha256: str
    model_revision: int
    run_request: RunRequest
    program_snapshot: Program
    active_parameters: dict[str, float]
    model_refs: tuple[Ref, ...]
    model_assumptions: tuple[str, ...]
    inputs: tuple[EvidenceRef, ...]
    input_source_ids: tuple[str, ...]
    outcome_origins: tuple[Origin, ...]
    points: tuple[SealedPoint, ...]
    artifact_sha256: str
    profile_snapshot: dict[str, JsonValue]
    status: Literal["payload-durable; confirmation-required"] = "payload-durable; confirmation-required"


class SealConfirmation(Record):
    forecast_id: Identifier
    seal_sha256: str
    acknowledgement_observed_at: datetime
    status: Literal["local-prospective", "late-confirmation"]
    clock_assumption: Text
    artifact_sha256: str


class ForecastReceipt(Record):
    seal: ForecastSeal
    confirmation: SealConfirmation | None


class Measurement(Record):
    measurement_schema: Literal["edi.measurement/1.0"]
    variable: Identifier
    observed_at: datetime
    unit: Identifier
    status: Literal["observed", "missing", "left-censored", "right-censored", "interval-censored"]
    value: Scalar | bool | None = None
    lower: Scalar | None = None
    upper: Scalar | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def consistent(self):
        if self.observed_at.utcoffset() is None:
            raise ValueError("measurement event time must be timezone aware")
        if self.status == "observed":
            if self.value is None or self.lower is not None or self.upper is not None:
                raise ValueError("observed measurement needs exactly one value")
        else:
            if self.value is not None or not self.reason:
                raise ValueError("missing/censored data needs a reason and no invented scalar")
            if self.status == "left-censored" and (self.upper is None or self.lower is not None):
                raise ValueError("left censoring needs an upper bound")
            if self.status == "right-censored" and (self.lower is None or self.upper is not None):
                raise ValueError("right censoring needs a lower bound")
            if self.status == "interval-censored" and (self.lower is None or self.upper is None or self.lower >= self.upper):
                raise ValueError("interval censoring needs ordered bounds")
            if self.status == "missing" and (self.lower is not None or self.upper is not None):
                raise ValueError("missing data cannot hide censoring bounds")
        return self


class CompareRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    assessment_id: Identifier
    forecast_id: Identifier
    outcome_watermark: int = Field(ge=0)
    rationale: Text


class PointAssessment(Record):
    point: SealedPoint
    status: Literal["scored", "missing", "censored", "ineligible", "invalid", "scan-incomplete"]
    evidence: EvidenceRef | None = None
    observation: Measurement | None = None
    source_id: str | None = None
    scores: dict[str, float] = Field(default_factory=dict)
    within_declared_limit: bool | None = None
    issues: tuple[str, ...]


class Comparison(Record):
    request: CompareRequest
    created_at: datetime
    forecast: ForecastReceipt
    outcome_watermark: int
    results: tuple[PointAssessment, ...]
    source_coverage: tuple[dict[str, JsonValue], ...]
    summaries: dict[str, JsonValue]
    possible_causes: dict[Cause, Literal["not-established"]]
    limitations: tuple[str, ...]
    usage: dict[str, JsonValue]
    artifact_sha256: str
    profile_snapshot: dict[str, JsonValue]
    qualification: Literal["local held-out assessment only; independent scientific validity unqualified"] = "local held-out assessment only; independent scientific validity unqualified"


class CauseHypothesis(Record):
    category: Cause
    explanation: Text
    status: Literal["candidate", "unknown"] = "candidate"
    support: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    counterevidence: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    discriminating_test: Text
    uncertainty: Text


class ReviewRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    review_id: Identifier
    assessment_id: Identifier
    model_revision: int = Field(ge=0)
    targets: tuple[Ref, ...] = Field(min_length=1, max_length=16)
    recommendation: Literal["retain", "revise", "reject", "investigate"]
    causes: tuple[CauseHypothesis, ...] = Field(min_length=1, max_length=16)
    retained_rivals: tuple[Text, ...] = Field(min_length=1, max_length=16)
    expected_benefit: Text
    new_verification_burden: Text
    rationale: Text
    candidates: tuple[Put, ...] = Field(default=(), max_length=16)
    attribution: Text


class RevisionReview(Record):
    request: ReviewRequest
    created_at: datetime
    assessment_sha256: str
    dependent_views: tuple[DependencyView, ...]
    target_snapshot: tuple[dict[str, JsonValue], ...]
    limitations: tuple[str, ...]
    artifact_sha256: str


class FindingRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    finding_id: Identifier
    review_id: Identifier
    newness_priority_basis: Text
    affected_parties: tuple[Text, ...] = Field(min_length=1, max_length=16)
    goal: Text
    horizon: Text
    chain: tuple[Text, ...] = Field(min_length=1, max_length=16)
    chain_status: Literal["hypothesized", "associative", "mixed-unverified"]
    support: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    counterevidence: tuple[EvidenceRef, ...] = Field(default=(), max_length=32)
    alternatives: tuple[Text, ...] = Field(min_length=1, max_length=16)
    uncertainty: Text
    suggested_action_class: Literal["observe", "investigate", "simulate", "review-policy"]
    expiry: datetime
    review_trigger: Text
    attribution: Text

    @model_validator(mode="after")
    def aware(self):
        if self.expiry.utcoffset() is None: raise ValueError("finding expiry needs an aware datetime")
        return self


class Finding(Record):
    request: FindingRequest
    created_at: datetime
    review_sha256: str
    status: Literal["draft; C0 controls delivery and C7 controls adoption"] = "draft; C0 controls delivery and C7 controls adoption"
    artifact_sha256: str


class YieldRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    yield_id: Identifier
    inquiry_id: Identifier
    assessment_ids: tuple[Identifier, ...] = Field(min_length=1, max_length=32)
    selection_basis: Text
    declared_exposure: int = Field(ge=1)
    resource_account: dict[str, JsonValue]
    caveats: tuple[Text, ...] = Field(min_length=1, max_length=16)


class YieldReview(Record):
    request: YieldRequest
    created_at: datetime
    assessment_hashes: tuple[str, ...]
    coverage: dict[str, JsonValue]
    calibrated_advantage: Literal["not-established; matched outcomes/control/cost validation required"] = "not-established; matched outcomes/control/cost validation required"
    artifact_sha256: str


class SubmissionRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    review_id: Identifier
    reason: Annotated[str, Field(min_length=1, max_length=4096)]


class StagedSubmission(Record):
    request: SubmissionRequest
    patch: WorldPatch


class SubmissionReceipt(Record):
    request: SubmissionRequest
    commit: WorldCommit


class ArtifactCursor(Record):
    kind: Literal["comparison", "review", "finding", "yield"]
    watermark: int = Field(ge=0)
    after: int = Field(ge=0)
    workspace_id: Identifier


class ArtifactPage(Record):
    items: tuple[dict[str, JsonValue], ...]
    next_cursor: ArtifactCursor | None
    status: Literal["bounded snapshot; not evidence of absence outside selection"] = "bounded snapshot; not evidence of absence outside selection"
