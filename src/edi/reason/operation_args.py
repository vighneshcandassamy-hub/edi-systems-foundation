"""Domain-neutral C0 argument grammar; authority and execution remain native C0/C7."""
import copy
import json

from edi.agency.benchmark import PublicIntent
from edi.analyze.contracts import CompileRequest, RunRequest
from edi.reason.contracts import EvidenceSelection, Response, YieldAssessment

TRIGGERS=("novel","unresolved","consequential","student-escalation")


def validate_arguments(operation, arguments):
    """Reject malformed envelopes before they can become dispatched proposals."""
    if operation=="world-call":
        PublicIntent.model_validate_json(json.dumps(arguments,allow_nan=False))
    elif operation=="acquire-asset":
        if set(arguments)!={"document_id"} or not isinstance(arguments["document_id"],str):
            raise ValueError("acquire-asset arguments are exactly {document_id: string}")
    elif operation=="select-context":
        if set(arguments)!={"evidence","world_ids"} or not isinstance(arguments["evidence"],list) or not isinstance(arguments["world_ids"],list):
            raise ValueError("select-context needs evidence and world_ids arrays")
        if len(arguments["evidence"])>16 or len(arguments["world_ids"])>16 or any(not isinstance(x,str) for x in arguments["world_ids"]):
            raise ValueError("selected context exceeds native bounds")
        for item in arguments["evidence"]:
            EvidenceSelection.model_validate_json(json.dumps(item,allow_nan=False))
    elif operation in ("analysis-compile","analysis-run"):
        cls=CompileRequest if operation=="analysis-compile" else RunRequest
        cls.model_validate_json(json.dumps(arguments,allow_nan=False))
    elif operation=="component-call":
        from edi.inquiry.operations import validate_call
        validate_call(arguments)
    elif operation=="teacher-review":
        if set(arguments)!={"trigger"} or arguments["trigger"] not in TRIGGERS:
            raise ValueError("teacher-review requires one valid trigger")
    elif operation=="yield":
        if set(arguments)-{"reason", "assessment"} or ("reason" in arguments and not isinstance(arguments["reason"],str)):
            raise ValueError("yield accepts a reason string and a typed assessment")
        if "assessment" in arguments:
            YieldAssessment.model_validate_json(json.dumps(arguments["assessment"], allow_nan=False))


def generation_schema(*, controller_policy="legacy"):
    """Native content schema with transport-owned identities supplied after serving."""
    schema=copy.deepcopy(Response.model_json_schema())
    supplied={"workspace_id","inquiry_id","request_id","response_id","job_id","context_sha256",
              "origin","attribution","binding","input_tokens","output_tokens","procedural_guidance"}
    for key in supplied:
        schema["properties"].pop(key,None)
    schema["required"]=[x for x in schema.get("required",[]) if x not in supplied]
    definitions=schema.setdefault("$defs",{})
    def native(model):
        value=copy.deepcopy(model.model_json_schema())
        for key,definition in value.pop("$defs",{}).items():
            if key in definitions and definitions[key]!=definition:
                raise ValueError("Conflicting native grammar definition: "+key)
            definitions[key]=definition
        return value
    def obj(properties,required):
        return {"type":"object","properties":properties,"required":required,"additionalProperties":False}
    arguments={
        "world-call":native(PublicIntent),
        "acquire-asset":obj({"document_id":{"type":"string"}},["document_id"]),
        "select-context":obj({
            "evidence":{"type":"array","items":native(EvidenceSelection),"maxItems":16},
            "world_ids":{"type":"array","items":{"type":"string"},"maxItems":16}},["evidence","world_ids"]),
        "analysis-compile":native(CompileRequest),
        "analysis-run":native(RunRequest),
        "teacher-review":obj({"trigger":{"type":"string","enum":list(TRIGGERS)}},["trigger"]),
        "yield":obj({"reason":{"type":"string"}, "assessment":native(YieldAssessment)},[])
    }
    if controller_policy == "information-seeking/1.0":
        arguments["yield"]["properties"]["reason"]["minLength"] = 1
        arguments["yield"]["properties"]["reason"]["maxLength"] = 8192
        arguments["yield"]["required"] = ["reason", "assessment"]
    elif controller_policy != "legacy":
        raise ValueError("unsupported controller policy")
    from edi.inquiry.operations import call_schema
    arguments["component-call"], component_definitions = call_schema()
    definitions.update(component_definitions)
    definitions["OperationProposal"]={"anyOf":[obj({
        "schema_version":{"const":"1.0","type":"string"},
        "operation":{"const":operation,"type":"string"},
        "arguments":shape},["operation","arguments"]) for operation,shape in arguments.items()]}
    return schema


def serving_schema(*, evidence_references=None, controller_turn=False, controller_policy="legacy"):
    """vLLM decoding envelope; native validation still enforces every key bound.

    vLLM 0.21 rejects propertyNames. Only the known native Identifier map-key
    length constraint is deferred to native validation, never to C0 dispatch.
    Operation names/shapes, values and all other generated constraints remain.
    """
    def compatible(value):
        if isinstance(value, dict):
            value = {key: compatible(item) for key, item in value.items()}
            if "propertyNames" in value:
                if value["propertyNames"] != {"minLength": 1, "maxLength": 256}:
                    raise ValueError("Unsupported new native map-key constraint")
                value.pop("propertyNames")
            return value
        if isinstance(value, list):
            return [compatible(item) for item in value]
        return value
    schema = compatible(generation_schema(controller_policy=controller_policy))
    if controller_turn:
        schema["properties"]["operation_proposals"]["minItems"] = 1
        if "operation_proposals" not in schema["required"]:
            schema["required"].append("operation_proposals")
    if evidence_references is not None:
        from edi.shared.contracts import EvidenceRef
        references = [EvidenceRef.model_validate_json(json.dumps(ref, allow_nan=False)).model_dump(mode="json")
                      for ref in evidence_references]
        if references:
            # Address choices are exactly the complete references already in the
            # pinned context, including lineage; no output is silently rewritten.
            schema["$defs"]["EvidenceRef"] = {"enum": references}
        else:
            def empty_support(value):
                if isinstance(value, dict):
                    if value.get("items") == {"$ref": "#/$defs/EvidenceRef"}:
                        value["maxItems"] = 0
                    for item in value.values(): empty_support(item)
                elif isinstance(value, list):
                    for item in value: empty_support(item)
            empty_support(schema)
    return schema
