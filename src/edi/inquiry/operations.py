"""Finite C0-mediated access to existing component operations.

These contracts expose existing ports, not new domain capabilities. Operator
admission, adoption, reconciliation, raw intake and recursive job control are
intentionally absent from model-generated requests.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field

from edi.shared.contracts import Identifier, Record
from edi.shared.durable_io import canonical
from edi.shared.errors import EDIError, ErrorCode


class OperationRead(Record):
    operation: Identifier


class Empty(Record):
    pass


class DerivationRead(Record):
    derivation_id: Identifier


class WorldRead(Record):
    record_id: Identifier
    revision: int | None = Field(default=None, ge=0)


class DependencyRead(WorldRead):
    direction: Literal["dependencies", "dependents"] = "dependencies"
    max_depth: int = Field(default=1, ge=1, le=8)


class InquiryRead(Record):
    inquiry_id: Identifier


class RunRead(Record):
    run_id: Identifier


class CompiledRead(Record):
    compiled_id: Identifier


class PolicyRead(Record):
    revision: int | None = Field(default=None, ge=0)


class ExecutionRead(Record):
    execution_id: Identifier


class AssessmentRead(Record):
    kind: Literal["forecast", "comparison", "review", "finding"]
    artifact_id: Identifier


class FindingRead(Record):
    finding_id: Identifier


@lru_cache(maxsize=1)
def contracts():
    # Lazy imports avoid C4's native-response contract importing its orchestrator.
    from edi.agency import contracts as agency
    from edi.analyze import contracts as analyze
    from edi.assess import contracts as assess
    from edi.interpret import contracts as interpret
    from edi.world.contracts import WorldCursor, WorldQuery
    from edi.observe.contracts import ReplayCursor

    class ObservationSelection(Record):
        cursor: ReplayCursor | None = None
        origin_ref: Identifier | None = None
        limit: int = Field(default=25, ge=1, le=100)

    class WorldSelection(Record):
        query: WorldQuery | None = None
        revision: int | None = Field(default=None, ge=0)
        cursor: WorldCursor | None = None
        limit: int = Field(default=25, ge=1, le=100)

    class AssessmentSelection(Record):
        kind: Literal["comparison", "review", "finding", "yield"]
        cursor: assess.ArtifactCursor | None = None
        limit: int = Field(default=25, ge=1, le=100)

    return {
        "describe-operation": OperationRead,
        "observation-records": ObservationSelection,
        "coverage": Empty,
        "interpret": interpret.InterpretRequest,
        "interpret-get": DerivationRead,
        "interpret-submit": interpret.SubmissionRequest,
        "world-head": Empty, "world-get": WorldRead,
        "world-query": WorldSelection, "world-dependencies": DependencyRead,
        "reason-get": InquiryRead, "reason-rank": InquiryRead,
        "reason-assessments": AssessmentSelection,
        "analysis-compile": analyze.CompileRequest,
        "analysis-run": analyze.RunRequest,
        "analysis-get": RunRead, "analysis-get-compiled": CompiledRead,
        "assess-seal": assess.SealRequest, "assess-compare": assess.CompareRequest,
        "assess-review": assess.ReviewRequest, "assess-finding": assess.FindingRequest,
        "assess-yield": assess.YieldRequest, "assess-submit": assess.SubmissionRequest,
        "assess-query": AssessmentSelection, "assess-get": AssessmentRead,
        "deliver-finding": FindingRead,
        "agency-propose": agency.AmendmentRequest,
        "agency-policy": PolicyRead, "agency-check": agency.ActionRequest,
        "agency-dispatch": agency.DispatchRequest, "agency-receipt": ExecutionRead,
        "agency-access": agency.AccessRequest, "agency-actor-view": agency.ActorViewRequest,
        "agency-archive": agency.ReportRequest, "agency-submit": agency.ModelUpdateRequest,
    }


IDENTITIES = frozenset(("workspace_id", "request_id", "world_request_id"))


def native_arguments(operation, arguments, *, workspace_id="c0-validation", request_id="c0-validation"):
    model = contracts().get(operation)
    if model is None:
        raise EDIError(ErrorCode.DENIED, "operation is outside the model-accessible component catalogue")
    if not isinstance(arguments, dict) or IDENTITIES.intersection(arguments):
        raise EDIError(ErrorCode.DENIED, "C0 supplies workspace and command identities")
    data = dict(arguments)
    for key in IDENTITIES.intersection(model.model_fields):
        data[key] = workspace_id if key == "workspace_id" else request_id
    return model.model_validate_json(canonical(data))


def validate_call(arguments):
    if not isinstance(arguments, dict) or set(arguments) != {"operation", "arguments"}:
        raise ValueError("component-call requires operation and arguments only")
    native_arguments(arguments["operation"], arguments["arguments"])


def call_schema():
    """Namespace native definitions; unrelated owners reuse some class names."""
    definitions, variants = {}, []
    for operation, model in contracts().items():
        schema = model.model_json_schema()
        prefix = "C0_" + operation.replace("-", "_") + "_"
        names = set(schema.get("$defs", {}))
        def rewrite(value):
            if isinstance(value, dict):
                return {key: ("#/$defs/" + prefix + item[8:] if key == "$ref" and isinstance(item, str)
                        and item.startswith("#/$defs/") and item[8:] in names else rewrite(item))
                        for key, item in value.items()}
            if isinstance(value, list): return [rewrite(item) for item in value]
            return value
        schema = rewrite(schema)
        definitions.update({prefix + name: definition for name, definition in schema.pop("$defs", {}).items()})
        for key in IDENTITIES:
            schema.get("properties", {}).pop(key, None)
        schema["required"] = [key for key in schema.get("required", []) if key not in IDENTITIES]
        variants.append({"type": "object", "properties": {
            "operation": {"type": "string", "const": operation}, "arguments": schema},
            "required": ["operation", "arguments"], "additionalProperties": False})
    return {"anyOf": variants}, definitions


def invoke(runtime, operation, arguments, request_id, *, assistance=None):
    from edi.inquiry.contracts import WorkflowStep
    if operation == "describe-operation":
        selected = arguments.get("operation")
        if selected not in contracts():
            raise EDIError(ErrorCode.NOT_FOUND, "component operation unavailable")
        schema = contracts()[selected].model_json_schema()
        for key in IDENTITIES:
            schema.get("properties", {}).pop(key, None)
        schema["required"] = [key for key in schema.get("required", []) if key not in IDENTITIES]
        return {"operation": selected, "arguments_schema": schema,
            "authority": "Existing native port through C0; identities supplied by C0; no operator admission/adoption"}
    data = dict(arguments)
    if operation == "interpret":
        for name in ("annotations", "associations"):
            if data.get(name):
                if assistance is None:
                    raise EDIError(ErrorCode.DENIED, "model-supplied interpretation needs actual response attribution")
                data[name] = [{**item, "method": "imported-assistance",
                    "assistance_lineage": assistance["lineage"], "assistance": assistance["provenance"]} for item in data[name]]
    if assistance is not None and "attribution" in contracts()[operation].model_fields:
        data["attribution"] = "C4-generated assistance: " + assistance["response_id"]
    request = native_arguments(operation, data, workspace_id=runtime.profile.workspace_id, request_id=request_id)
    if operation == "observation-records":
        return runtime.reader_for("C0").replay(**{key: getattr(request, key) for key in ("cursor", "origin_ref", "limit")})
    return runtime.workflow.invoke_component(WorkflowStep(step_id=request_id, operation=operation,
        arguments=request.model_dump(mode="json", exclude={"schema_version"})))
