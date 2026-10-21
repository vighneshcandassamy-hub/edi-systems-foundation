"""C0 workflow data, never executable templates or capability grants."""
from pathlib import Path
from typing import Literal

from pydantic import Field, JsonValue, model_validator

from edi.shared.contracts import Identifier, Record

Operation = Literal[
    "register-origin", "observe-json", "observe-bytes", "coverage", "interpret", "interpret-submit", "interpret-get",
    "world-propose", "world-commit", "world-get", "world-head", "world-ack", "world-query", "world-dependencies", "world-status",
    "reason-investigate", "reason-step", "reason-export", "reason-import", "reason-submit", "reason-frontier", "reason-ack", "reason-assessments", "reason-get", "reason-rank",
    "analysis-compile", "analysis-run", "analysis-control", "analysis-status", "analysis-get", "assess-seal", "assess-compare", "assess-review", "assess-finding", "assess-yield", "assess-submit", "assess-query", "assess-get",
    "agency-propose", "agency-adopt", "agency-policy", "agency-check", "agency-dispatch", "agency-receipt", "agency-access", "agency-access-disposition", "agency-actor-view", "agency-archive", "agency-reconcile", "agency-submit",
    "deliver-finding",
]


class WorkflowProfile(Record):
    profile_id: Identifier = "local-workflow-v1"
    workspace_id: Identifier = "default"
    database: Path = Field(default_factory=lambda: Path(".local/workflows.sqlite3"))
    trusted_operator_steps: bool = False
    operator_ids: tuple[Identifier, ...] = Field(default=("local-operator",), min_length=1, max_length=16)
    max_plan_bytes: int = Field(default=512 * 1024, ge=1024)
    max_input_bytes: int = Field(default=256 * 1024, ge=1024)
    max_step_bytes: int = Field(default=4 * 1024**2, ge=65536)
    max_stored_bytes: int = Field(default=256 * 1024**2, ge=65536)
    max_records: int = Field(default=10000, ge=4)
    max_resume_seconds: float = Field(default=30.0, gt=0, le=300)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)


class OutcomeCondition(Record):
    path: str = Field(max_length=2048)
    equals: JsonValue


class WorkflowStep(Record):
    step_id: Identifier
    operation: Operation
    arguments: dict[str, JsonValue] = Field(default_factory=dict)
    require: tuple[OutcomeCondition, ...] = Field(default=(), max_length=8)


class WorkflowSpec(Record):
    workspace_id: Identifier
    workflow_id: Identifier
    purpose: str = Field(min_length=1, max_length=8192)
    scope_and_horizon: str = Field(min_length=1, max_length=8192)
    evaluation_standards: tuple[str, ...] = Field(min_length=1, max_length=16)
    assumptions: tuple[str, ...] = Field(min_length=1, max_length=32)
    attribution: str = Field(min_length=1, max_length=8192)
    steps: tuple[WorkflowStep, ...] = Field(min_length=1, max_length=96)

    @model_validator(mode="after")
    def unique(self):
        if len({s.step_id for s in self.steps}) != len(self.steps):
            raise ValueError("workflow step IDs must be unique")
        return self


class WorkflowInput(Record):
    workspace_id: Identifier
    workflow_id: Identifier
    input_id: Identifier
    value: JsonValue
    attribution: str = Field(min_length=1, max_length=8192)
    authority: Literal["data", "operator-decision"] = "data"
    operator_id: Identifier | None = None


class WorkflowOperatorInput(WorkflowInput):
    authority: Literal["operator-decision"] = "operator-decision"
    operator_id: Identifier


class WorkflowStatus(Record):
    workspace_id: Identifier
    workflow_id: Identifier
    state: Literal["ready", "waiting-input", "uncertain-completion", "failed", "completed", "cancelled", "yielded"]
    completed_steps: tuple[Identifier, ...]
    next_step: str | None
    waiting_input: str | None = None
    error: dict[str, JsonValue] | None = None
    outputs: dict[str, JsonValue]
    plan_sha256: str
    qualification: Literal["scoped-workflow-only; component/scientific-qualification-open"] = "scoped-workflow-only; component/scientific-qualification-open"
