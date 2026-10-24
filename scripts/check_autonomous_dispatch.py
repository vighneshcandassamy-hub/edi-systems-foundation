"""Authored native C0/C1/C2/C4/C7 dispatch regression; zero model inference."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import secrets
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "examples/autonomous" if (ROOT / "examples/autonomous").exists() else ROOT))
from neutral_world import MISSION, start_world
from edi.agency.benchmark import SimulationGrant
from edi.agency.config import AgencyProfile
from edi.inquiry.benchmark import Investigation
from edi.inquiry.runtime import Runtime
from edi.observe.benchmark import BrokerConnector, http_json
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import ModelBinding, OperationProposal, Response
from edi.shared.config import LocalProfile
from edi.shared.durable_io import canonical, digest
from edi.shared.errors import EDIError, ErrorCode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binding = ModelBinding(model_id="authored-dispatch-fixture", revision="v1",
        provider="authored-no-provider", engine="fixture", tokenizer_revision="fixture-v1")
    class AuthoredGateway:
        def __init__(self):
            self.binding, self.calls = binding, 0
        def complete(self, job, episode):
            access = episode.request.controller_access
            assert access is not None and access.operations == MISSION["public_operations"]
            assert access.mission_sha256 == digest(MISSION)
            turn = int(episode.request.inquiry_id.rsplit(":", 1)[1])
            mission_record = episode.context.evidence[0].reference.record_id
            decisions = [
                {"operation": "acquire-asset", "arguments": {"document_id": mission_record}},
                {"operation": "world-call", "arguments": {"operation": "sources", "body": {}}},
                {"operation": "world-call", "arguments": {"operation": "read", "body": {"document_id": "m17"}}},
                {"operation": "world-call", "arguments": {"operation": "submit", "body": {"conclusion": "Authored dispatch fixture only; not model reasoning or scientific evidence."}}}]
            self.calls += 1
            return Response.model_validate_json(json.dumps({"workspace_id": episode.request.workspace_id,
                "inquiry_id": episode.request.inquiry_id, "request_id": "fixture:" + job.job_id,
                "response_id": "fixture:" + job.job_id, "job_id": job.job_id,
                "context_sha256": job.context_sha256, "origin": "human-authored",
                "attribution": "Authored fixed operation sequence for dispatch regression; zero inference",
                "binding": binding.model_dump(mode="json"), "input_tokens": 0, "output_tokens": 0,
                "rationale_summary": "Authored native dispatch fixture", "limitation": "No autonomous reasoning claim",
                "operation_proposals": [decisions[turn]]}))
    example = OperationProposal.model_validate_json(json.dumps({"operation": "world-call", "arguments": {"operation": "sources", "body": {}}}))
    assert digest(["run", 1, example]) == digest(["run", 1, example.model_dump(mode="json")])
    assert canonical({"result": example}) == canonical({"result": example.model_dump(mode="json")})
    try: canonical({"unsupported": object()})
    except TypeError: pass
    else: raise AssertionError("Unsupported objects must not be stringified")
    with tempfile.TemporaryDirectory(prefix="edi-native-dispatch-") as directory:
        root, workspace = Path(directory), "dispatch-fixture"
        token = secrets.token_urlsafe(32)
        server = start_world(root, token)
        gateway = AuthoredGateway()
        now = datetime.now(timezone.utc)
        grant = SimulationGrant.model_validate_json(json.dumps({"grant_id": workspace,
            "session_id": workspace, "workspace_id": workspace, "endpoint": "http://127.0.0.1:8098",
            "token_sha256": hashlib.sha256(token.encode()).hexdigest(), "mission_sha256": digest(MISSION),
            "operator_id": "fixture-operator", "not_before": (now - timedelta(seconds=1)).isoformat(),
            "expires_at": (now + timedelta(minutes=5)).isoformat(), "operations": list(MISSION["public_operations"]),
            "maximum_requests": 32}))
        requests = []
        def transport(url, body, headers, **kwargs):
            requests.append(url.rsplit("/", 1)[1])
            if url.endswith("/status"):
                raise EDIError(ErrorCode.UNAVAILABLE, "Authored response loss after dispatch fence")
            return http_json(url, body, headers, **kwargs)
        def reopen():
            runtime = Runtime(LocalProfile(workspace_id=workspace, database=root / "owners.sqlite3"),
                reasoning_profile=ReasoningProfile(workspace_id=workspace, database=root / "owners.reason.sqlite3", student=binding),
                agency_profile=AgencyProfile(workspace_id=workspace, database=root / "owners.agency.sqlite3", operator_ids=("fixture-operator",)))
            authority = runtime.agency_for("C0").benchmark_authority(grant, endpoint=grant.endpoint,
                token_sha256=grant.token_sha256, workspace_id=workspace, session_id=workspace)
            connector = BrokerConnector(runtime, grant.endpoint, token, workspace, authority,
                runtime.workflow.profile.database, max_requests=32, transport=transport)
            return Investigation(runtime, connector, gateway, runtime.workflow.profile.database,
                "dispatch-regression", controller_policy="information-seeking/1.0", max_turns=8, max_tokens=262144)
        try:
            controller = reopen()
            state = controller.step()
            assert requests == ["mission", "read"], requests
            assert state["state"] == "ready"
            feedback = []
            for item in state["evidence"]:
                raw = controller.runtime.observation.read_payload(item["record_id"], length=item["length"])
                try: value = json.loads(raw)
                except (ValueError, UnicodeError): continue
                if isinstance(value, dict) and value.get("operation") == "acquire-asset:error": feedback.append(value)
            assert feedback and feedback[0]["result"]["message"] == "asset read failed; original response retained", feedback
            assert "OperationProposal is not JSON serializable" not in json.dumps(feedback)
            for expected in ("sources", "read", "submit"):
                before = len(requests)
                controller = reopen()
                assert len(requests) == before, "Construction replayed a request"
                state = controller.step()
                assert requests[-1] == expected and len(requests) == before + 1, (expected, requests)
            assert state["state"] == "completed", state
            before = len(requests)
            controller = reopen()
            assert controller.step() == state and len(requests) == before
            # Exercise the other corrected digest site: an unresolved world call
            # must remain unknown, never become an ordinary tool error/retry.
            proposal = OperationProposal.model_validate_json(json.dumps({"operation": "world-call",
                "arguments": {"operation": "status", "body": {}}}))
            try:
                controller._dispatch_known(proposal, {**state, "turn": 7}, "authored-fault")
            except EDIError as exc:
                assert exc.code == ErrorCode.UNKNOWN_COMMIT, exc
            else: raise AssertionError("Unresolved broker dispatch became a known result")
            report = {"scope": "authored fixed operation sequence; native integration regression, not autonomous model qualification",
                "passed": True, "nested_native_values_canonical": True, "unsupported_objects_rejected": True, "model_calls": 0, "authored_gateway_calls": gateway.calls,
                "public_request_order": requests, "invalid_asset_reached_broker": True,
                "native_asset_error_returned": True, "sources_read_submit_reached_broker": True,
                "C2_interpretation_returned": True, "terminal_reopen_no_redispatch": True,
                "unresolved_broker_call_preserved_unknown": True, "adopted_access_description_reaches_C4": True}
        finally:
            server.shutdown()
            server.server_close()
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
