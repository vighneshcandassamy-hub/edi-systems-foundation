"""Targeted native controller-contract regression; authored fixtures, zero inference."""
import argparse
import copy
import hashlib
from io import BytesIO
import json
from pathlib import Path
import tempfile

import jsonschema
import xgrammar

from edi.inquiry.runtime import Runtime
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import InquiryRequest, ModelBinding, Response, StepRequest
from edi.reason.gateway import VllmBackend, render_job_messages
from edi.reason.operation_args import serving_schema
from edi.shared.config import LocalProfile
from edi.shared.errors import EDIError


def validate(cls, value):
    return cls.model_validate_json(json.dumps(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = {}
    binding = ModelBinding(model_id="authored-controller-contract", revision="fixture-v1",
        provider="authored-no-provider", engine="authored-fixture", tokenizer_revision="fixture-v1")

    def forbidden(*args, **kwargs):
        raise AssertionError("Contract checks must not contact a provider")

    for mode in ("controller-turn", "proposal"):
        with tempfile.TemporaryDirectory(prefix="edi-controller-contract-") as directory:
            root, workspace = Path(directory), "contract-fixture"
            runtime = Runtime(LocalProfile(workspace_id=workspace, database=root / "owners.sqlite3"),
                reasoning_profile=ReasoningProfile(workspace_id=workspace,
                    database=root / "owners.reason.sqlite3", student=binding))
            origin = runtime.register_origin(OriginSpec(namespace="authored.contract.fixture", native_source_id=mode,
                epoch="1", deliverer="contract-check", channel="fixture", adapter="authored",
                binding_basis="configured"))
            payload = b'{"fixture":true}'
            receipt = runtime.observe(Capture(origin_ref=origin.origin_ref, idempotency_key="fixture",
                kind="contract-fixture", media_type="application/json", origin_class="simulation",
                lineage=("authored-contract-fixture",), expected_bytes=len(payload),
                expected_sha256=hashlib.sha256(payload).hexdigest()), BytesIO(payload))
            inquiry = validate(InquiryRequest, {"workspace_id": workspace, "inquiry_id": "i", "request_id": "i",
                "question": "Verify a wire contract", "purpose": "Authored contract check only",
                "scope": "No scientific or model result", "horizon": "One fixture",
                "response_mode": mode, "model_revision": runtime.world.head(),
                "evidence": [{"record_id": receipt.observation.record_id, "offset": 0, "length": len(payload)}]})
            runtime.reasoning.investigate(inquiry)
            episode = runtime.reasoning.step(StepRequest(workspace_id=workspace, inquiry_id="i",
                request_id="j", action="student", reason="Authored fixture; no dispatch"))
            job = episode.jobs[-1]
            messages, _ = render_job_messages(runtime, binding, job, episode)
            backend = VllmBackend("http://127.0.0.1:8008", binding.model_id, transport=forbidden,
                completion_timeout=600)
            compact, compact_images = render_job_messages(runtime, binding, job, episode, schema_in_transport=True)
            assert compact[1] == messages[1], "transport compaction changed the native data cut"
            assert compact_images == []
            if mode == "controller-turn":
                original_control = json.loads(messages[0]["content"])
                compact_control = json.loads(compact[0]["content"])
                assert "response_schema" not in compact_control
                assert "response_fields" in compact_control
                for key in original_control.keys() - {"response_schema"}:
                    assert original_control[key] == compact_control[key]
                assert len(compact[0]["content"]) < len(messages[0]["content"])
                results["transport-schema-index"] = "native data and other control identical; full decoder retained"
            assert backend.generation_schema_for(compact) == backend.generation_schema_for(messages)
            schema = backend.generation_schema_for(compact)
            xgrammar.Grammar.from_json_schema(json.dumps(schema))
            content = {"rationale_summary": "Authored fixture", "limitation": "No inference or factual finding"}
            reference = episode.context.evidence[0].reference.model_dump(mode="json")
            if mode == "controller-turn":
                content["operation_proposals"] = [{"operation": "yield", "arguments": {"reason": "Contract check"}}]
                content["hypotheses"] = [{"hypothesis_id": "h1", "claim": "Authored claim",
                    "mechanism": "Unmeasured", "scope": "Fixture", "applicability": "Unknown",
                    "unknowns": ["No empirical claim"], "support": [reference]}]
                assert json.loads(messages[0]["content"])["controller_turn"]["question"] == inquiry.question
            jsonschema.Draft202012Validator(schema).validate(content)

            def response(value):
                return validate(Response, {**value, "workspace_id": workspace, "inquiry_id": "i",
                    "request_id": "response", "response_id": "response", "job_id": job.job_id,
                    "context_sha256": job.context_sha256, "origin": "human-authored",
                    "attribution": "Authored contract fixture; no model call",
                    "binding": binding.model_dump(mode="json")})

            runtime.reasoning.validate_response(response(content))
            if mode == "controller-turn":
                for kind in ("missing-operation", "missing-lineage"):
                    bad = copy.deepcopy(content)
                    if kind == "missing-operation":
                        bad.pop("operation_proposals")
                    else:
                        bad["hypotheses"][0]["support"][0].pop("lineage")
                    try:
                        jsonschema.Draft202012Validator(schema).validate(bad)
                    except jsonschema.ValidationError:
                        pass
                    else:
                        raise AssertionError("Decoder schema accepted " + kind)
                    try:
                        runtime.reasoning.validate_response(response(bad))
                    except EDIError:
                        pass
                    else:
                        raise AssertionError("Native admission accepted " + kind)
                    results[kind] = "rejected by both wire schema and native admission"
            results[mode] = "valid content compiled and passed native validation"
    empty = serving_schema(evidence_references=[], controller_turn=True)
    xgrammar.Grammar.from_json_schema(json.dumps(empty))
    jsonschema.Draft202012Validator(empty).validate({"rationale_summary": "Authored empty cut",
        "limitation": "No evidence", "operation_proposals": [{"operation": "yield", "arguments": {"reason": "Empty cut"}}]})
    results["empty-cut"] = "grammar compiled; explicit yield valid without fabricated support"
    report = {"scope": "authored native contract fixtures; not model/investigation qualification",
        "passed": True, "model_calls": 0, "provider_contacts": 0, "results": results}
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
