"""Local JSON control plane; payload bytes never pass through JSON serialization."""
import argparse
import json
from pathlib import Path
import sys

from pydantic import ValidationError

from edi.inquiry.runtime import Runtime
from edi.inquiry.contracts import WorkflowInput, WorkflowOperatorInput, WorkflowProfile, WorkflowSpec
from edi.agency.config import AgencyProfile
from edi.agency.contracts import (
    AccessDispositionRequest, AccessRequest, ActionRequest, ActorViewRequest, AdoptionRequest,
    AmendmentRequest, DispatchRequest, ModelUpdateRequest, ReconcileRequest, ReportRequest,
)
from edi.agency.contracts import ArtifactCursor as AgencyArtifactCursor
from edi.analyze.config import AnalysisProfile
from edi.analyze.contracts import CompileRequest, RunControl, RunRequest
from edi.assess.config import AssessmentProfile
from edi.assess.contracts import ArtifactCursor, CompareRequest, FindingRequest, ReviewRequest, SealRequest, YieldRequest
from edi.assess.contracts import SubmissionRequest as AssessmentSubmissionRequest
from edi.interpret.config import InterpretationProfile
from edi.interpret.contracts import InterpretRequest, SubmissionRequest
from edi.observe.contracts import Capture, OriginSpec, ReplayCursor
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import FrontierUpdate, InquiryRequest, OutboxAck, Response, StepRequest
from edi.reason.contracts import SubmissionRequest as ReasonSubmissionRequest
from edi.shared.config import LocalProfile
from edi.shared.errors import EDIError, ErrorCode
from edi.world.config import WorldProfile
from edi.world.contracts import WorldCursor, WorldPatch, WorldQuery


def _parser():
    parser = argparse.ArgumentParser(prog="edi", description="EDI local C1-C7 runtime (unqualified)")
    parser.add_argument("--config", type=Path, help="LocalProfile JSON; must include workspace_id/database")
    parser.add_argument("--database", type=Path, help="override local database path")
    parser.add_argument("--workspace", help="override workspace scope")
    parser.add_argument("--world-config", type=Path, help="WorldProfile JSON; default is a separate sibling database")
    parser.add_argument("--interpret-config", type=Path, help="InterpretationProfile JSON; default is a separate sibling database")
    parser.add_argument("--reason-config", type=Path, help="ReasoningProfile JSON; default is a separate sibling database")
    parser.add_argument("--analysis-config", type=Path, help="AnalysisProfile JSON; default is a separate sibling database")
    parser.add_argument("--assessment-config", type=Path, help="AssessmentProfile JSON; default is a separate sibling database")
    parser.add_argument("--agency-config", type=Path, help="AgencyProfile JSON; trusted local operator surface, separate sibling database")
    parser.add_argument("--workflow-config", type=Path, help="C0 WorkflowProfile JSON; operator steps disabled by default")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities")
    p = sub.add_parser("register-origin")
    p.add_argument("spec", type=Path)
    p = sub.add_parser("ingest")
    p.add_argument("capture", type=Path)
    p.add_argument("payload", type=Path)
    p = sub.add_parser("get")
    p.add_argument("record_id")
    p = sub.add_parser("origin")
    p.add_argument("origin_ref")
    p = sub.add_parser("status")
    p.add_argument("origin_ref")
    p.add_argument("idempotency_key")
    p = sub.add_parser("replay")
    p.add_argument("--cursor", type=Path, help="previous page's cursor object, saved as JSON")
    p.add_argument("--origin")
    p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("read")
    p.add_argument("record_id")
    p.add_argument("output", type=Path)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--length", type=int, default=65536)
    p = sub.add_parser("checkpoint")
    p.add_argument("consumer")
    p.add_argument("--position", type=int, help="omit to read current checkpoint")
    sub.add_parser("coverage")
    p = sub.add_parser("backup")
    p.add_argument("destination", type=Path)
    sub.add_parser("world-head")
    for command in ("world-propose", "world-commit"):
        p = sub.add_parser(command)
        p.add_argument("patch", type=Path)
    p = sub.add_parser("world-get")
    p.add_argument("record_id")
    p.add_argument("--revision", type=int)
    p = sub.add_parser("world-query")
    p.add_argument("--query", type=Path)
    p.add_argument("--cursor", type=Path)
    p.add_argument("--revision", type=int)
    p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("world-dependencies")
    p.add_argument("record_id")
    p.add_argument("--revision", type=int)
    p.add_argument("--direction", choices=("dependencies", "dependents"), default="dependencies")
    p.add_argument("--depth", type=int, default=1)
    p = sub.add_parser("world-status")
    p.add_argument("request_id")
    for command in ("world-progress", "world-ack"):
        p = sub.add_parser(command)
        p.add_argument("consumer")
    p = sub.add_parser("interpret")
    p.add_argument("request", type=Path)
    p = sub.add_parser("derivation")
    p.add_argument("derivation_id")
    for command in ("interpret-build-patch", "interpret-submit"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    for command in ("reason-investigate", "reason-step", "reason-import-response", "reason-frontier-update",
                    "reason-build-patch", "reason-submit", "reason-outbox-ack"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    for command in ("reason-get", "reason-rank-frontier"):
        p = sub.add_parser(command)
        p.add_argument("inquiry_id")
        if command == "reason-get":
            p.add_argument("--sequence", type=int, help="immutable episode version; omit for current")
    p = sub.add_parser("reason-status")
    p.add_argument("operation", choices=("investigate", "step", "response", "frontier", "outbox-ack", "submission-stage", "submission-receipt"))
    p.add_argument("request_id")
    p = sub.add_parser("reason-export-job")
    p.add_argument("inquiry_id")
    p.add_argument("job_id")
    for command in ("analysis-compile", "analysis-run", "analysis-control"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    for command, key in (("analysis-get-compiled", "compiled_id"), ("analysis-get-run", "run_id"), ("analysis-status", "request_id")):
        p = sub.add_parser(command)
        p.add_argument(key)
    for command in ("assess-seal", "assess-compare", "assess-review", "assess-finding", "assess-yield", "assess-build-patch", "assess-submit"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    for command in ("assess-get-forecast", "assess-get-comparison", "assess-get-review", "assess-get-finding"):
        p = sub.add_parser(command)
        p.add_argument("artifact_id")
    p = sub.add_parser("assess-query")
    p.add_argument("kind", choices=("comparison", "review", "finding", "yield"))
    p.add_argument("--cursor", type=Path)
    p.add_argument("--limit", type=int, default=25)
    for command in ("agency-propose-policy", "agency-decide-policy", "agency-check", "agency-dispatch",
                    "agency-actor-view", "agency-access", "agency-access-disposition", "agency-archive-report",
                    "agency-reconcile", "agency-build-patch", "agency-submit"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    p = sub.add_parser("agency-policy")
    p.add_argument("--revision", type=int)
    for command in ("agency-receipt", "agency-get-amendment", "agency-get-decision", "agency-get-view", "agency-get-access"):
        p = sub.add_parser(command)
        p.add_argument("artifact_id")
    p = sub.add_parser("agency-query")
    p.add_argument("kind", choices=("amendment", "adoption", "decision", "execution-intent", "execution-receipt", "actor-view", "access", "access-disposition", "report-archive", "model-receipt"))
    p.add_argument("--cursor", type=Path)
    p.add_argument("--limit", type=int, default=25)
    for command in ("workflow-create", "workflow-supply", "workflow-supply-operator"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
    for command in ("workflow-resume", "workflow-status", "workflow-output", "workflow-cancel"):
        p = sub.add_parser(command)
        p.add_argument("workflow_id")
        if command == "workflow-output": p.add_argument("step_id")
        if command == "workflow-resume": p.add_argument("--retry-uncertain", action="store_true", help="explicit trusted-local recovery after the prior runner is known stopped")
    p = sub.add_parser("workflow-attempts")
    p.add_argument("workflow_id")
    p.add_argument("step_id")
    p.add_argument("--after", type=int, default=0)
    p.add_argument("--limit", type=int, default=25)
    return parser


def _emit(value):
    if isinstance(value, tuple):
        value = [item.model_dump(mode="json") for item in value]
    elif hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    print(json.dumps(value, ensure_ascii=False, allow_nan=False))


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        profile = LocalProfile.model_validate_json(args.config.read_bytes()) if args.config else LocalProfile()
        overrides = profile.model_dump()
        if args.database is not None:
            overrides["database"] = args.database
        if args.workspace is not None:
            overrides["workspace_id"] = args.workspace
        world_profile = WorldProfile.model_validate_json(args.world_config.read_bytes()) if args.world_config else None
        interpretation_profile = InterpretationProfile.model_validate_json(args.interpret_config.read_bytes()) if args.interpret_config else None
        reasoning_profile = ReasoningProfile.model_validate_json(args.reason_config.read_bytes()) if args.reason_config else None
        analysis_profile = AnalysisProfile.model_validate_json(args.analysis_config.read_bytes()) if args.analysis_config else None
        assessment_profile = AssessmentProfile.model_validate_json(args.assessment_config.read_bytes()) if args.assessment_config else None
        agency_profile = AgencyProfile.model_validate_json(args.agency_config.read_bytes()) if args.agency_config else None
        workflow_profile = WorkflowProfile.model_validate_json(args.workflow_config.read_bytes()) if args.workflow_config else None
        runtime = Runtime(LocalProfile.model_validate(overrides), world_profile, interpretation_profile, reasoning_profile, analysis_profile, assessment_profile, agency_profile, workflow_profile)
        obs = runtime.observation
        world = runtime.world if args.command.startswith("world-") else None
        if args.command == "capabilities":
            _emit(runtime.capabilities())
        elif args.command == "register-origin":
            _emit(runtime.register_origin(OriginSpec.model_validate_json(args.spec.read_bytes())))
        elif args.command == "ingest":
            _emit(runtime.observe_file(Capture.model_validate_json(args.capture.read_bytes()), args.payload))
        elif args.command == "get":
            _emit(obs.get_record(args.record_id))
        elif args.command == "origin":
            _emit(obs.get_origin(args.origin_ref))
        elif args.command == "status":
            _emit(obs.commit_status(args.origin_ref, args.idempotency_key))
        elif args.command == "replay":
            cursor = ReplayCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
            _emit(obs.replay(cursor=cursor, origin_ref=args.origin, limit=args.limit))
        elif args.command == "read":
            data = obs.read_payload(args.record_id, offset=args.offset, length=args.length)
            with args.output.open("xb") as target:
                target.write(data)
            _emit({"status": "written", "bytes": len(data), "output": str(args.output)})
        elif args.command == "checkpoint":
            position = (obs.get_checkpoint(args.consumer) if args.position is None
                        else obs.checkpoint(args.consumer, args.position))
            _emit({"consumer": args.consumer, "position": position})
        elif args.command == "coverage":
            _emit(obs.coverage())
        elif args.command == "backup":
            obs.backup(args.destination)
            _emit({"status": "copied", "destination": str(args.destination), "qualification": "not-run"})
        elif args.command == "world-head":
            _emit({"revision": world.head(), "workspace_id": runtime.profile.workspace_id})
        elif args.command in ("world-propose", "world-commit"):
            patch = WorldPatch.model_validate_json(args.patch.read_bytes())
            _emit(world.propose_patch(patch) if args.command == "world-propose" else world.commit(patch))
        elif args.command == "world-get":
            _emit(world.get(args.record_id, revision=args.revision))
        elif args.command == "world-query":
            query = WorldQuery.model_validate_json(args.query.read_bytes()) if args.query else None
            cursor = WorldCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
            _emit(world.query(query, revision=args.revision, cursor=cursor, limit=args.limit))
        elif args.command == "world-dependencies":
            _emit(world.dependencies(args.record_id, revision=args.revision,
                                     direction=args.direction, max_depth=args.depth))
        elif args.command == "world-status":
            result = world.commit_status(args.request_id)
            _emit(result if result is not None else {"status": "not-found", "request_id": args.request_id})
        elif args.command == "world-progress":
            _emit({"consumer": args.consumer, "position": world.consumer_position(args.consumer)})
        elif args.command == "world-ack":
            _emit({"consumer": args.consumer, "position": runtime.acknowledge_world_progress(args.consumer)})
        elif args.command == "interpret":
            _emit(runtime.interpretation.interpret(InterpretRequest.model_validate_json(args.request.read_bytes())))
        elif args.command == "derivation":
            _emit(runtime.interpretation.get_derivation(args.derivation_id))
        elif args.command in ("interpret-build-patch", "interpret-submit"):
            request = SubmissionRequest.model_validate_json(args.request.read_bytes())
            result = (runtime.interpretation.build_patch(request) if args.command == "interpret-build-patch"
                      else runtime.interpretation.submit(request))
            _emit(result)
        elif args.command.startswith("reason-"):
            reason = runtime.reasoning
            if args.command == "reason-get":
                _emit(reason.get(args.inquiry_id, sequence=args.sequence))
            elif args.command == "reason-rank-frontier":
                _emit(reason.rank_frontier(args.inquiry_id))
            elif args.command == "reason-status":
                result = reason.request_status(args.operation, args.request_id)
                _emit(result if result is not None else {"status": "not-found", "request_id": args.request_id})
            elif args.command == "reason-export-job":
                _emit(reason.export_job(args.inquiry_id, args.job_id))
            else:
                commands = {
                    "reason-investigate": (InquiryRequest, reason.investigate),
                    "reason-step": (StepRequest, reason.step),
                    "reason-import-response": (Response, reason.import_response),
                    "reason-frontier-update": (FrontierUpdate, reason.update_frontier),
                    "reason-outbox-ack": (OutboxAck, reason.acknowledge_outbox),
                    "reason-build-patch": (ReasonSubmissionRequest, reason.build_patch),
                    "reason-submit": (ReasonSubmissionRequest, reason.submit),
                }
                contract, method = commands[args.command]
                _emit(method(contract.model_validate_json(args.request.read_bytes())))
        elif args.command.startswith("analysis-"):
            analysis = runtime.analysis
            if args.command == "analysis-get-compiled":
                _emit(analysis.get_compiled(args.compiled_id))
            elif args.command == "analysis-get-run":
                _emit(analysis.get_run(args.run_id))
            elif args.command == "analysis-status":
                result = analysis.status(args.request_id)
                _emit(result if result is not None else {"status": "not-found", "request_id": args.request_id})
            else:
                commands = {"analysis-compile": (CompileRequest, analysis.compile),
                            "analysis-run": (RunRequest, analysis.run_scenario),
                            "analysis-control": (RunControl, analysis.control_run)}
                contract, method = commands[args.command]
                _emit(method(contract.model_validate_json(args.request.read_bytes())))
        elif args.command.startswith("assess-"):
            assessment = runtime.assessment
            if args.command == "assess-query":
                cursor = ArtifactCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
                _emit(assessment.query(args.kind, cursor=cursor, limit=args.limit))
            elif args.command.startswith("assess-get-"):
                methods = {"assess-get-forecast": assessment.get_forecast, "assess-get-comparison": assessment.get_comparison,
                           "assess-get-review": assessment.get_review, "assess-get-finding": assessment.get_finding}
                _emit(methods[args.command](args.artifact_id))
            else:
                commands = {"assess-seal": (SealRequest, assessment.seal_forecast),
                    "assess-compare": (CompareRequest, assessment.compare_outcome),
                    "assess-review": (ReviewRequest, assessment.review_revision),
                    "assess-finding": (FindingRequest, assessment.draft_finding),
                    "assess-yield": (YieldRequest, assessment.review_inquiry_yield),
                    "assess-build-patch": (AssessmentSubmissionRequest, assessment.build_patch),
                    "assess-submit": (AssessmentSubmissionRequest, assessment.submit_revision)}
                contract, method = commands[args.command]
                _emit(method(contract.model_validate_json(args.request.read_bytes())))
        elif args.command.startswith("agency-"):
            agency = runtime.agency
            if args.command == "agency-policy":
                _emit(agency.read_policy(args.revision))
            elif args.command == "agency-query":
                cursor = AgencyArtifactCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
                _emit(agency.query(args.kind, cursor=cursor, limit=args.limit))
            elif args.command in ("agency-receipt", "agency-get-amendment", "agency-get-decision", "agency-get-view", "agency-get-access"):
                methods = {"agency-receipt": agency.get_receipt, "agency-get-amendment": agency.get_amendment,
                    "agency-get-decision": agency.get_decision, "agency-get-view": agency.get_actor_view,
                    "agency-get-access": agency.get_access}
                _emit(methods[args.command](args.artifact_id))
            else:
                commands = {"agency-propose-policy": (AmendmentRequest, agency.request_adoption),
                    "agency-decide-policy": (AdoptionRequest, agency.decide_adoption),
                    "agency-check": (ActionRequest, agency.check_action),
                    "agency-dispatch": (DispatchRequest, agency.dispatch_authorized),
                    "agency-actor-view": (ActorViewRequest, agency.qualify_actor_view),
                    "agency-access": (AccessRequest, agency.review_access_scope),
                    "agency-access-disposition": (AccessDispositionRequest, agency.record_access_disposition),
                    "agency-archive-report": (ReportRequest, agency.archive_report),
                    "agency-reconcile": (ReconcileRequest, agency.reconcile_execution),
                    "agency-build-patch": (ModelUpdateRequest, agency.build_model_patch),
                    "agency-submit": (ModelUpdateRequest, agency.submit_model_update)}
                contract, method = commands[args.command]
                _emit(method(contract.model_validate_json(args.request.read_bytes())))
        elif args.command.startswith("workflow-"):
            workflow = runtime.workflow
            if args.command == "workflow-create": _emit(workflow.create(WorkflowSpec.model_validate_json(args.request.read_bytes())))
            elif args.command == "workflow-supply": _emit(workflow.supply(WorkflowInput.model_validate_json(args.request.read_bytes())))
            elif args.command == "workflow-supply-operator": _emit(workflow.supply_operator(WorkflowOperatorInput.model_validate_json(args.request.read_bytes())))
            elif args.command == "workflow-resume": _emit(workflow.resume(args.workflow_id, retry_uncertain=args.retry_uncertain))
            elif args.command == "workflow-output": _emit(workflow.output(args.workflow_id, args.step_id))
            elif args.command == "workflow-attempts": _emit(workflow.attempts(args.workflow_id, args.step_id, after=args.after, limit=args.limit))
            elif args.command == "workflow-cancel": _emit(workflow.cancel(args.workflow_id))
            else: _emit(workflow.status(args.workflow_id))
        return 0
    except EDIError as exc:
        print(json.dumps(exc.as_dict()), file=sys.stderr)
    except (ValidationError, ValueError, OSError) as exc:
        print(json.dumps(EDIError(ErrorCode.INVALID, str(exc)).as_dict()), file=sys.stderr)
    return 2
