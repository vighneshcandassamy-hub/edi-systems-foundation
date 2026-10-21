"""Versioned C5 stock/flow IR and immutable conditional run contracts."""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.shared.contracts import EvidenceRef, Identifier, Record, TimeValue
from edi.world.contracts import DependencyView, Ref, StoredRepresentation

Text = Annotated[str, Field(min_length=1, max_length=8192)]
Scalar = Annotated[float, Field(allow_inf_nan=False)]


class Unit(Record):
    symbol: Identifier
    dimensions: dict[Identifier, Annotated[int, Field(ge=-8, le=8)]] = Field(default_factory=dict)
    basis: Literal["SI", "declared-domain"] = "SI"
    # Coherent units only; scaling/offset conversion is never inferred.

    @model_validator(mode="after")
    def bounded(self):
        if len(self.dimensions) > 16 or any(power == 0 for power in self.dimensions.values()):
            raise ValueError("unit dimensions must have at most sixteen nonzero powers")
        return self


class Node(Record):
    node_id: Identifier
    operator: Literal["constant", "read", "add", "subtract", "multiply", "divide", "negate", "min", "max", "lookup"]
    inputs: tuple[Identifier, ...] = Field(default=(), max_length=2)
    value: Scalar | None = None
    symbol: Identifier | None = None
    unit: Unit | None = None
    x_unit: Unit | None = None
    y_unit: Unit | None = None
    points: tuple[tuple[Scalar, Scalar], ...] = Field(default=(), max_length=128)
    extrapolation: Literal["error", "clamp"] = "error"


class StockSpec(Record):
    symbol: Identifier
    world_ref: Ref
    unit: Unit
    lower: Scalar | None = None
    upper: Scalar | None = None

    @model_validator(mode="after")
    def ordered(self):
        if self.lower is not None and self.upper is not None and self.lower >= self.upper:
            raise ValueError("stock upper bound must exceed lower bound")
        return self


class Parameter(Record):
    symbol: Identifier
    value: Scalar
    unit: Unit
    lower: Scalar
    upper: Scalar

    @model_validator(mode="after")
    def domain(self):
        if not self.lower <= self.value <= self.upper:
            raise ValueError("parameter default must lie in its declared domain")
        return self


class Driver(Parameter):
    """External piecewise-constant boundary input, not an inferred causal driver."""


class FlowSpec(Record):
    symbol: Identifier
    world_ref: Ref
    rate_node: Identifier
    source: Identifier | None = None
    sink: Identifier | None = None


class Program(Record):
    ir_version: Literal["edi.stock-flow-ir/1.0"] = "edi.stock-flow-ir/1.0"
    stocks: tuple[StockSpec, ...] = Field(min_length=1, max_length=32)
    parameters: tuple[Parameter, ...] = Field(default=(), max_length=64)
    drivers: tuple[Driver, ...] = Field(default=(), max_length=32)
    nodes: tuple[Node, ...] = Field(min_length=1, max_length=256)
    flows: tuple[FlowSpec, ...] = Field(min_length=1, max_length=64)
    required_capabilities: tuple[Identifier, ...] = Field(default=(), max_length=16)
    time_unit: Literal["s"] = "s"
    history_semantics: Literal["stock-state-only"] = "stock-state-only"
    assumptions: tuple[Text, ...] = Field(min_length=1, max_length=32)
    formalization_rationale: Text
    source_equation_status: Literal["authored-formalization", "source-transcription", "proposed-correction"]
    source_statement: Text


class CompileRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    model_revision: int = Field(ge=0)
    mechanism_ref: Ref
    use_policy: Literal["accepted-for-use", "candidate-exploration"] = "accepted-for-use"
    rationale: Text


class Diagnostic(Record):
    code: Identifier
    severity: Literal["info", "warning", "error"]
    message: Text
    target: str | None = None


class CompiledModel(Record):
    compiled_id: Identifier
    request: CompileRequest
    created_at: datetime
    compiler: Literal["edi.stock-flow-compiler/1.0"] = "edi.stock-flow-compiler/1.0"
    status: Literal["supported", "unsupported"]
    program: Program | None
    node_order: tuple[str, ...] = ()
    world: tuple[StoredRepresentation, ...] = ()
    dependencies: tuple[DependencyView, ...] = ()
    diagnostics: tuple[Diagnostic, ...]
    context_sha256: str
    artifact_sha256: str
    profile_snapshot: dict[str, JsonValue]
    qualification: Literal["source-only; runtime unqualified"] = "source-only; runtime unqualified"


class DriverSchedule(Record):
    symbol: Identifier
    points: tuple[tuple[Scalar, Scalar], ...] = Field(min_length=1, max_length=128)


class Variation(Record):
    name: Identifier
    parameter_values: dict[Identifier, Scalar]


class Correspondence(Record):
    stock_symbol: Identifier
    observation_channel: Text
    aggregation: Literal["instantaneous-state"] = "instantaneous-state"
    limitation: Text


class ScenarioSpec(Record):
    scenario_id: Identifier
    start: Scalar
    end: Scalar
    output_times: tuple[Scalar, ...] = Field(min_length=2, max_length=2000)
    time_origin: TimeValue = Field(default_factory=TimeValue)
    initial_state: dict[Identifier, Scalar]
    parameters: dict[Identifier, Scalar] = Field(default_factory=dict)
    drivers: tuple[DriverSchedule, ...] = Field(default=(), max_length=32)
    variations: tuple[Variation, ...] = Field(default=(), max_length=8)
    correspondence: tuple[Correspondence, ...] = Field(default=(), max_length=32)
    evidence: tuple[EvidenceRef, ...] = Field(default=(), max_length=16)
    actor_information_masks: tuple[dict[str, JsonValue], ...] = Field(default=(), max_length=16)
    terminal_obligations: tuple[Text, ...] = Field(default=(), max_length=32)
    assumptions: tuple[Text, ...] = Field(min_length=1, max_length=32)
    rationale: Text

    @model_validator(mode="after")
    def clock(self):
        if self.end <= self.start or self.output_times[0] != self.start or self.output_times[-1] != self.end:
            raise ValueError("output grid must include ordered scenario endpoints")
        if any(b <= a for a, b in zip(self.output_times, self.output_times[1:])):
            raise ValueError("output times must be strictly increasing")
        return self


class SolverSpec(Record):
    backend: Literal["scipy.solve_ivp"] = "scipy.solve_ivp"
    scipy_version: Literal["1.17.0"] = "1.17.0"
    numpy_version: Literal["2.5.3"] = "2.5.3"
    method: Literal["RK45", "DOP853", "Radau", "BDF"] = "RK45"
    rtol: float = Field(default=1e-6, ge=1e-12, le=1e-2)
    atol: float = Field(default=1e-9, ge=1e-15, le=1e-2)
    max_step: float = Field(gt=0)
    bound_tolerance: float = Field(default=1e-8, ge=0, le=1e-2)


class RunRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    run_id: Identifier
    compiled_id: Identifier
    mode: Literal["numerical", "qualitative"]
    scenario: ScenarioSpec
    solver: SolverSpec | None = None
    inquiry_id: str | None = None
    test_id: str | None = None


class RunControl(Record):
    workspace_id: Identifier
    request_id: Identifier
    run_request_id: Identifier
    action: Literal["cancel", "interrupt"]
    reason: Text
    expected_attempt: Identifier | None = None


class Trajectory(Record):
    variant: Identifier
    status: Literal["completed", "partial", "failed"]
    times: tuple[float, ...]
    states: dict[str, tuple[float, ...]]
    cumulative_transfers: dict[str, tuple[float, ...]]
    final_time: float
    parameter_values: dict[str, float]
    balance_residuals: dict[str, float]
    diagnostics: tuple[Diagnostic, ...]
    nfev: int = Field(ge=0)


class RunRecord(Record):
    request: RunRequest
    compiled: CompiledModel
    created_at: datetime
    finished_at: datetime
    implementation: Literal["edi-c5/0.6.0"] = "edi-c5/0.6.0"
    status: Literal["completed", "partial", "unsupported", "failed", "cancelled", "interrupted"]
    trajectories: tuple[Trajectory, ...]
    scenario_envelope: dict[str, JsonValue]
    finite_differences: tuple[dict[str, JsonValue], ...]
    diagnostics: tuple[Diagnostic, ...]
    evidence_metadata: tuple[dict[str, JsonValue], ...]
    runtime_versions: dict[str, str]
    usage: dict[str, JsonValue]
    artifact_sha256: str
    profile_snapshot: dict[str, JsonValue]
    origin_class: Literal["simulation"] = "simulation"
    forecast_seal: Literal["unsealed; C6 prospective registration required"] = "unsealed; C6 prospective registration required"
    qualification: Literal["source-only; runtime unqualified"] = "source-only; runtime unqualified"
