"""Controlled C0-C7 walkthrough. Authored scheduling/model; real bound inference.

Stages run in separate processes. No scientific/autonomous capability claim.
Only the declared run directory is used; no benchmark/evaluator resources.
"""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import traceback
from datetime import datetime, timedelta, timezone

from edi.agency.config import AgencyProfile
from edi.inquiry.runtime import Runtime
from edi.inquiry.application import ApplicationProfile, IntegratedApplication
from edi.inquiry.contracts import WorkflowProfile, WorkflowSpec, WorkflowInput, WorkflowOperatorInput
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import ModelBinding, RejectedResponse
from edi.reason.gateway import NativeGateway, VllmBackend
from edi.reason.exchange import TeacherExchangeGateway, AwaitingModelResponse, ModelOutputRejected
from edi.shared.config import LocalProfile

REV = "0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
W = "engineering-20261022"
ATTR = "Authored engineering harness; explicit local operator; not autonomous discovery"
ROOT = Path(os.environ.get("EDI_ENGINEERING_ROOT", "/kaggle/working/edi-engineering-20261022"))
ROOT.mkdir(parents=True, exist_ok=True)


def now(): return datetime.now(timezone.utc)
def plain(v): return v.model_dump(mode="json") if hasattr(v, "model_dump") else v
def save(name, value):
    data = (json.dumps(plain(value), indent=2, sort_keys=True) + "\n").encode()
    path = ROOT / name
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError("immutable artifact differs: " + name)
    if not path.exists(): path.write_bytes(data)
    return value
def read(name): return json.loads((ROOT / name).read_bytes())
def validate(cls, data): return cls.model_validate_json(json.dumps(data))
def ref(record_id, version=1): return {"record_id": record_id, "version": version}
def clock(value): return {"status": "known", "value": value.isoformat(), "reason": None}


def runtime(models=True):
    student = ModelBinding(model_id="Qwen/Qwen3-VL-8B-Instruct", revision=REV,
        provider="local-vllm", engine="vllm/0.21.0", tokenizer_revision=REV)
    teacher = ModelBinding(model_id="ChatGPT-current-session-operator-declared",
        revision="engineering-critique-20261022", provider="manual-file-exchange",
        engine="current-assistant-session-unverified", tokenizer_revision="unmeasured")
    r = Runtime(LocalProfile(workspace_id=W, database=ROOT / "owners.sqlite3"),
        reasoning_profile=ReasoningProfile(workspace_id=W, database=ROOT / "owners.reason.sqlite3",
            student=student, teacher=teacher),
        agency_profile=AgencyProfile(workspace_id=W, database=ROOT / "owners.agency.sqlite3", operator_ids=("engineering-operator",)),
        workflow_profile=WorkflowProfile(workspace_id=W, database=ROOT / "owners.workflows.sqlite3",
            trusted_operator_steps=True, operator_ids=("engineering-operator",)))
    if models:
        profile_path = ROOT / "application.json"
        if not profile_path.exists():
            n = now()
            profile = {"application_id": W, "run_id": "controlled-engineering",
                "observation": plain(r.profile), "reasoning": plain(r.reasoning.profile), "workflow": plain(r.workflow.profile), "agency": plain(r.agency.profile),
                "student": {"binding": plain(student), "max_images": 0},
                "teacher": {"binding": plain(teacher), "directory": str(ROOT / "teacher-exchange"),
                    "attribution": "Current ChatGPT session critique; operator-declared identity, implementation context known"},
                "broker": {"grant": {"grant_id": W, "session_id": W, "workspace_id": W, "endpoint": "http://127.0.0.1:8098",
                    "token_sha256": hashlib.sha256(os.environ["EDI_BROKER_TOKEN"].encode()).hexdigest(),
                    "mission_sha256": hashlib.sha256(b"Controlled engineering fixture").hexdigest(), "operator_id": "engineering-operator",
                    "not_before": (n-timedelta(seconds=1)).isoformat(), "expires_at": (n+timedelta(hours=3)).isoformat(),
                    "operations": ["mission", "status"], "maximum_requests": 10}}, "max_turns": 8, "max_tokens": 98304}
            save("application.json", profile)
        app = IntegratedApplication(ApplicationProfile.load(profile_path))
        r = app.runtime
        from edi.agency.benchmark import PublicIntent
        received = app.investigation.connector.call(PublicIntent(operation="status", body={"request_id": "engineering-status"}))
        if received["http_status"] != 200: raise RuntimeError("Neutral broker connection failed")
        save("broker-connection.json", received)
        return r, app.investigation.student, app.teacher
    return r


def op(r, name, operation, arguments, require=(), operator=False):
    """Each handoff is an immutable, restartable C0 workflow with explicit input."""
    spec = {"workspace_id": W, "workflow_id": name, "purpose": "One complete engineering integration campaign",
        "scope_and_horizon": "Controlled local file-size accumulator, one bounded run",
        "evaluation_standards": ["Native owner acceptance, retained provenance, explicit authority, honest limitations"],
        "assumptions": ["Scheduling and model are authored; model responses are not authored by harness"],
        "attribution": ATTR, "steps": [{"step_id": "handoff", "operation": operation,
            "arguments": {"$input": "arguments", "path": ""}, "require": list(require)}]}
    r.workflow.create(validate(WorkflowSpec, spec))
    cls = WorkflowOperatorInput if operator else WorkflowInput
    data = {"workspace_id": W, "workflow_id": name, "input_id": "arguments", "value": arguments, "attribution": ATTR}
    if operator: data["operator_id"] = "engineering-operator"
    request = validate(cls, data)
    (r.workflow.supply_operator if operator else r.workflow.supply)(request)
    status = r.workflow.resume(name)
    save(name + ".workflow.json", status)
    if status.state != "completed": raise RuntimeError(name + ": " + json.dumps(plain(status)))
    output = r.workflow.output(name, "handoff")
    save(name + ".json", output)
    print(name, "completed", flush=True)
    return output


def evidence(observation):
    return {"workspace_id": W, "record_id": observation["record_id"], "sha256": observation["manifest"]["sha256"],
        "origin_class": observation["capture"]["origin_class"], "lineage": observation["capture"]["lineage"]}


def student_attempt(r, s, name):
    episode = op(r, name + "-job", "reason-step", {"inquiry_id": "inquiry", "action": "student",
        "reason": "Bounded engineering reasoning; preserve uncertainty and address retained critique/rejections"})
    ep = r.reasoning.get("inquiry")
    job = ep.jobs[-1]
    try:
        response = r.reasoning.complete_job(job, ep)
        r.reasoning.validate_response(response)
    except Exception as error:
        receipt = s.receipt(job.job_id)
        save(name + "-failed.json", {"type": type(error).__name__, "error": str(error), "receipt": receipt})
        if receipt and receipt.get("raw_record_id"):
            rejection = validate(RejectedResponse, {"workspace_id": W, "inquiry_id": "inquiry", "request_id": name + "-reject",
                "job_id": job.job_id, "raw_record_id": receipt["raw_record_id"], "context_sha256": job.context_sha256,
                "diagnostic": str(error)[:8192], "input_tokens": receipt.get("input_tokens"), "output_tokens": receipt.get("output_tokens")})
            r.reasoning.reject_response(rejection)
        raise
    save(name + "-receipt.json", s.receipt(job.job_id))
    out = op(r, name + "-import", "reason-import", plain(response))
    return out


def initial():
    save("protocol.json", {"campaign": W, "source_commit": "0935ce5b9e6d1f66fbb6f8f8566afefddcfd05a8",
        "scope": "C0-C7 engineering walkthrough; not Meadows/autonomous/scientific qualification",
        "planned_handoffs": ["C1 intake", "C2 decode and candidate submission", "C3 explicit authored model admission",
            "C4 real student", "C4 exported teacher cut/imported critique", "C4 real student revision",
            "C5 compile and numerical run", "C6 prospective seal/OS-measured outcome/compare/review/candidate/finding",
            "C7 access/proposal/operator adoption/authorized read/denied external action/actor mask", "C0 delivery", "fresh-process restart and SQLite integrity"],
        "model": {"student": "Qwen/Qwen3-VL-8B-Instruct", "revision": REV, "weights": "fixed", "teacher": "current ChatGPT session, manual file exchange; identity not independently authenticated; implementation context known"},
        "budget": {"student_max_calls": 3, "teacher_imports": 1, "input_cap": 14336, "output_cap": 2048, "additional_paid_spend": 0},
        "outcome_protocol": "Authored 32-byte file held unchanged across a future nominal sampling epoch; actual OS stat and read times retained. External refers to OS measurement, not independent scientific provenance. Model 8+4*t is authored; expected discrepancy is intentionally controlled.",
        "clock_policy": "Bind UTC origin after model phase, target origin+5s at least 25s in future. Pre/post stat brackets target; only admit nominal event if file metadata identical across bracket. Retain actual acquisition times and declared constant-window mapping.",
        "pass_criteria": ["two real admitted student responses separated by retained teacher feedback", "C2 candidate retained", "C5 supported/completed", "C6 local-prospective and scored outcome", "C6 candidate-only revision retained", "C7 internal allowed/external denied", "fresh process replay does not invoke inference", "eight distinct DBs integrity ok"],
        "limitations": ["One scheduled scenario", "No autonomous component selection claim", "Teacher not blind", "No independent model superiority or Meadows result"]})
    r, s, t = runtime()
    origins = {}
    for channel in ("inputs", "outcomes"):
        origins[channel] = op(r, "origin-" + channel, "register-origin", {"namespace": "edi.engineering", "native_source_id": channel,
            "epoch": W, "deliverer": "local-file-stat", "channel": channel, "adapter": "engineering-harness/1.0", "binding_basis": "configured",
            "descriptor": {"same_host_dependence": True, "scientific_independence": "not established"}})
    if (ROOT / "input-record.json").exists():
        observed = read("input-record.json")["observation"]
    else:
        f = ROOT / "observed-input.bin"
        readings = []
        for n in (8, 12, 16):
            f.write_bytes(b"x" * n)
            readings.append({"relative_second": (n - 8) / 4, "bytes": f.stat().st_size, "acquired_at": now().isoformat()})
        observed = op(r, "input-record", "observe-json", {"capture": {"origin_ref": origins["inputs"]["origin_ref"],
            "origin_class": "external", "completeness": "complete", "profiles": {"controlled_writer": True}},
            "payload": {"readings": readings, "relative_second_basis": "authored sampling labels, not measured elapsed intervals",
                "limitation": "One controlled file on one host; writer uses configured sizes. No physical causal law inferred."}})["observation"]
    der = op(r, "interpret", "interpret", {"inputs": [{"record_id": observed["record_id"], "decoder": "json"}]},
        [{"path": "/derivation/status", "equals": "complete"}])
    op(r, "interpret-submit", "interpret-submit", {"derivation_id": der["derivation"]["derivation_id"], "base_revision": 0})
    base = read("model-admission.json")["previous_revision"] if (ROOT / "model-admission.json").exists() else r.world.head()
    unit = {"symbol": "byte", "dimensions": {"domain:byte": 1}, "basis": "declared-domain"}
    rate = {"symbol": "byte/s", "dimensions": {"domain:byte": 1, "s": -1}, "basis": "declared-domain"}
    ir = {"stocks": [{"symbol": "bytes", "world_ref": ref("byte-stock", base + 1), "unit": unit}],
        "flows": [{"symbol": "write", "world_ref": ref("byte-flow", base + 1), "rate_node": "rate", "sink": "bytes"}],
        "nodes": [{"node_id": "rate", "operator": "constant", "value": 4.0, "unit": rate}],
        "assumptions": ["Authored constant four bytes per second", "Initial eight bytes; controlled protocol may differ"],
        "formalization_rationale": "Exercise typed numerical owner contracts", "source_equation_status": "authored-formalization",
        "source_statement": "Harness-authored dB/dt=4; not discovered or independently validated"}
    structures = [("byte-stock", {"family": "stock", "quantity": {"status": "known", "value": 8, "scale": "cardinal", "unit": "byte"}, "inflows": [ref("byte-flow", None)]}),
        ("byte-flow", {"family": "flow-process", "participants": [{"ref": ref("byte-stock", None), "role": "sink", "direction": "in"}]}),
        ("byte-law", {"family": "response-relationship", "participants": [{"ref": ref("byte-stock", None), "role": "stock"}, {"ref": ref("byte-flow", None), "role": "flow"}], "mechanism": {"edi_ir_v1": ir}, "execution_status": "descriptive"}),
        ("operator-actor", {"family": "constituent", "roles": ["engineering operator"]})]
    ops = [{"operation": "put", "representation": {"record_id": rid, "structure": structure, "basis": "assumption", "support": [evidence(observed)],
        "assumptions": ["Authored engineering fixture"], "method_lineage": [ATTR]}, "expected_version": 0,
        "admission": {"decision": "accepted_for_use", "rationale": ATTR, "use_scope": "this controlled walkthrough",
            "verification_obligation": "No scientific truth established; compare held-out measurement"}} for rid, structure in structures]
    model = op(r, "model-admission", "world-commit", {"base_revision": base, "reason": ATTR, "change_kind": "explanation", "operations": ops}, operator=True)
    op(r, "inquiry-bounded-cut", "reason-investigate", {"inquiry_id": "inquiry", "question": "What do these controlled file readings support and fail to establish? Propose cautious hypotheses and useful observations. The labels are authored, not elapsed-time measurements. Keep response concise; tool proposals optional.",
        "purpose": "Real student reasoning in controlled engineering walkthrough", "scope": "Observed file readings only; authored model is an assumption",
        "horizon": "single short engineering session", "model_revision": model["revision"], "world_ids": ["byte-stock"],
        "evidence": [{"record_id": observed["record_id"], "length": min(4096, observed["manifest"]["byte_count"])}], "axes": ["evidence", "rivals", "learning"],
        "unknowns": ["True clock correspondence and unseen writer changes", "No independent repeat or causal identification"],
        "budget": {"rounds": 4, "jobs": 6, "reserved_tokens": 98304, "input_token_cap": 14336, "output_token_cap": 2048}})
    try: student_attempt(r, s, "student-initial")
    except Exception:
        if r.reasoning.get("inquiry").jobs[-1].status != "rejected": raise
        student_attempt(r, s, "student-initial-correction")
    teacher = op(r, "teacher-job", "reason-step", {"inquiry_id": "inquiry", "action": "teacher", "teacher_trigger": "unresolved",
        "reason": "Critique epistemic limits against original cut and actual student, before a real revision"})
    ep = r.reasoning.get("inquiry")
    try: r.reasoning.complete_job(ep.jobs[-1], ep)
    except AwaitingModelResponse as pending:
        save("teacher-pending.json", {"job_id": pending.job_id, "request_path": pending.request_path, "context_sha256": ep.context.sha256})
    save("initial-complete.json", {"status": "awaiting-explicit-teacher-import", "student_responses": len(ep.responses)})


def analysis_model_cut(r):
    """Pin opaque IR against native C3 versions, retaining the original model."""
    revision = read("model-admission.json")["revision"]
    port = r.world_for("C0")
    law = port.get("byte-law", revision=revision)
    representation = plain(law.representation)
    program = representation["structure"]["mechanism"]["edi_ir_v1"]
    changed = False
    for item in program["stocks"] + program["flows"]:
        selected = port.get(item["world_ref"]["record_id"], revision=revision)
        if item["world_ref"]["version"] != selected.version:
            item["world_ref"]["version"] = selected.version
            changed = True
    if changed:
        representation["method_lineage"].append("engineering-opaque-IR-version-repair")
        head = r.world.head()
        current = port.get("byte-law", revision=head)
        commit = op(r, "model-pin-repair", "world-commit", {"base_revision": head,
            "reason": "Correct opaque IR version pins to actual native C3 versions; equation and observations unchanged",
            "change_kind": "context", "operations": [{"operation": "put", "representation": representation,
                "expected_version": current.version, "admission": plain(law.admission)}]}, operator=True)
        revision = commit["revision"]
    return revision, ref("byte-law", port.get("byte-law", revision=revision).version), ref("operator-actor", port.get("operator-actor", revision=revision).version)


def finish():
    r, s, t = runtime()
    pending = read("teacher-pending.json")
    save("teacher-import-receipt.json", t.import_feedback(pending["job_id"], ROOT / "teacher-feedback.json"))
    ep = r.reasoning.get("inquiry")
    response = r.reasoning.complete_job(ep.jobs[-1], ep)
    r.reasoning.validate_response(response)
    op(r, "teacher-import", "reason-import", plain(response))
    student_attempt(r, s, "student-revised")
    ep = r.reasoning.get("inquiry")
    # Submit genuine student candidates only when actually returned.
    if ep.responses[-1].candidates:
        op(r, "student-candidates", "reason-submit", {"inquiry_id": "inquiry", "response_id": ep.responses[-1].response_id,
            "reason": "Actual student candidates retained without admission"})
    save("reasoning-final.json", r.reasoning.get("inquiry"))
    revision, law_ref, actor_ref = analysis_model_cut(r)
    compiled = op(r, "compile", "analysis-compile", {"model_revision": revision, "mechanism_ref": law_ref,
        "rationale": "Compile explicitly authored accepted-for-use engineering law"}, [{"path": "/status", "equals": "supported"}])
    origin = now() + timedelta(seconds=25)
    target = origin + timedelta(seconds=5)
    out_file = ROOT / "held-out.bin"
    out_file.write_bytes(b"y" * 32)
    before = {"at": now().isoformat(), "size": out_file.stat().st_size, "mtime_ns": out_file.stat().st_mtime_ns}
    save("clock-binding.json", {"origin": origin.isoformat(), "target": target.isoformat(), "before": before,
        "protocol": "Constant file across nominal epoch, not fabricated exact acquisition timestamp"})
    initial_record = read("input-record.json")["observation"]
    run = op(r, "numerical-run", "analysis-run", {"run_id": "run", "compiled_id": compiled["compiled_id"], "mode": "numerical",
        "scenario": {"scenario_id": "scenario", "start": 0.0, "end": 5.0, "output_times": [0.0, 5.0], "time_origin": clock(origin),
            "initial_state": {"bytes": 8.0}, "correspondence": [{"stock_symbol": "bytes", "observation_channel": "OS stat bytes",
                "limitation": "Authored model versus controlled constant file; future nominal epoch bracketed by stat reads"}],
            "evidence": [evidence(initial_record)], "assumptions": ["Fixed rate four; measurement apparatus shares same host"], "rationale": ATTR},
        "solver": {"max_step": 0.25}}, [{"path": "/status", "equals": "completed"}])
    outcome_origin = read("origin-outcomes.json")["origin_ref"]
    sealed = op(r, "forecast", "assess-seal", {"forecast_id": "forecast", "run_id": "run",
        "cases": [{"case_id": "bytes-at-five", "stock_symbol": "bytes", "relative_time": 5.0, "origin_ref": outcome_origin,
            "variable": "file-bytes", "declared_dependence_group": "same-controlled-host", "interpretation": "point", "score_limit": 1.0,
            "interpretation_basis": "Direct cardinal byte count; nominal epoch under constant-window clock mapping"}],
        "rule": {"source_independence_assumption": "Distinct origin IDs, common host and harness. Outcome OS stat is not copied from forecast; scientific independence NOT established."},
        "assumptions": ["Controlled writer sets 32 before seal and holds unchanged through epoch; neither model nor teacher receives outcome"],
        "rationale": "Prospective registration before target and before outcome capture"}, [{"path": "/confirmation/status", "equals": "local-prospective"}])
    remaining = (target - now()).total_seconds() + 0.25
    if remaining > 0: time.sleep(min(remaining, 40))
    actual = now()
    stat = out_file.stat()
    if actual < target or stat.st_size != before["size"] or stat.st_mtime_ns != before["mtime_ns"]:
        raise RuntimeError("Constant-window timestamp mapping not verified")
    save("outcome-acquisition.json", {"actual_read_at": actual.isoformat(), "nominal_event_at": target.isoformat(), "bytes": stat.st_size,
        "before": before, "after_mtime_ns": stat.st_mtime_ns, "jitter_seconds": (actual-target).total_seconds(),
        "mapping_assumption": "No writer between recorded brackets; unchanged mtime/size on controlled private file"})
    outcome = op(r, "outcome", "observe-json", {"capture": {"origin_ref": outcome_origin, "kind": "measurement-v1",
        "origin_class": "external", "lineage": [], "completeness": "complete",
        "time": {"event_time": clock(target), "reported_time": clock(actual), "clock_id": "UTC"},
        "profiles": {"controlled_fixture": True, "actual_acquisition_at": actual.isoformat(), "nominal_constant_window_mapping": True}},
        "payload": {"measurement_schema": "edi.measurement/1.0", "variable": "file-bytes", "observed_at": target.isoformat(),
            "unit": "byte", "status": "observed", "value": float(stat.st_size)}})
    coverage = op(r, "outcome-coverage", "coverage", {})
    watermark = coverage["watermark"]
    comparison = op(r, "compare", "assess-compare", {"assessment_id": "assessment", "forecast_id": "forecast", "outcome_watermark": watermark,
        "rationale": "Deterministic native first matching measurement; no favorable outcome selection"}, [{"path": "/results/0/status", "equals": "scored"}])
    candidate = {"representation": {"record_id": "review-candidate", "basis": "hypothesis", "structure": {"family": "constituent", "roles": ["unresolved discrepancy"]},
        "support": [evidence(outcome["observation"])], "assumptions": ["Engineering author requests writer audit; no causal conclusion"]}, "expected_version": 0}
    op(r, "review", "assess-review", {"review_id": "review", "assessment_id": "assessment", "model_revision": revision,
        "targets": [law_ref], "recommendation": "investigate", "causes": [{"category": "unexpected-drivers", "explanation": "Writer policy may differ from fixed-rate law",
            "discriminating_test": "Record writer commands and actual intervals in a separate future run", "uncertainty": "Single controlled discrepancy identifies no unique cause"}],
        "retained_rivals": ["Timestamp correspondence", "Wrong initial state or rate", "Writer changes"], "expected_benefit": "Locate discrepancy before changing law",
        "new_verification_burden": "Independent repeated acquisition", "rationale": ATTR, "candidates": [candidate], "attribution": ATTR})
    op(r, "assessment-candidate", "assess-submit", {"review_id": "review", "reason": "Retain explicitly authored candidate only"})
    op(r, "finding", "assess-finding", {"finding_id": "finding", "review_id": "review", "newness_priority_basis": "Controlled forecast error",
        "affected_parties": ["engineering operator"], "goal": "Verify component handoffs", "horizon": "this run", "chain": ["authored model", "measured discrepancy", "further inquiry"],
        "chain_status": "mixed-unverified", "support": [evidence(outcome["observation"])], "alternatives": ["Clock mapping", "Rate or writer mismatch"],
        "uncertainty": "No causal inference or autonomous discovery demonstrated", "suggested_action_class": "investigate", "expiry": (now()+timedelta(hours=1)).isoformat(),
        "review_trigger": "New independent measurement", "attribution": ATTR})
    n = now()
    policy = {"policy_id": "engineering-readonly", "purpose_version": "v1", "purpose": "Controlled engineering observations",
        "evaluation_standards": ["Exact origin read only; no external effects"], "assumptions": ["Explicit trusted local operator"],
        "grants": [{"grant_id": "read-outcomes", "operation": "select-observations", "origin_refs": [outcome_origin], "not_before": (n-timedelta(seconds=1)).isoformat(),
            "expires_at": (n+timedelta(hours=1)).isoformat(), "max_items": 10, "basis": ATTR}]}
    op(r, "access", "agency-access", {"access_id": "access", "scope": {"operation": "select-observations", "origin_refs": [outcome_origin], "max_items": 10},
        "target": "outcome-channel", "unknown": "Need read authority", "hypothesis_family": "engineering", "minimum_useful_evidence": "One outcome record", "rationale": ATTR, "attribution": ATTR})
    op(r, "policy-proposal", "agency-propose", {"amendment_id": "amendment", "expected_revision": 0, "proposed": policy, "change_kind": "bootstrap",
        "trigger": "Explicit engineering authority", "rationale": ATTR, "attribution": ATTR, "resource_and_implementation_basis": "Finite local native read"})
    op(r, "policy-adoption", "agency-adopt", {"amendment_id": "amendment", "expected_revision": 0, "decision": "adopt", "operator_id": "engineering-operator", "rationale": ATTR}, operator=True)
    action = {"decision_id": "read-decision", "policy_revision": 1, "purpose_version": "v1", "grant_id": "read-outcomes",
        "intent": {"operation": "select-observations", "origin_ref": outcome_origin, "limit": 10}, "rationale": ATTR,
        "expected_effects_and_limits": "Native read only, no physical actuation", "attribution": ATTR}
    op(r, "action-check", "agency-check", action, [{"path": "/status", "equals": "allowed"}])
    op(r, "authorized-read", "agency-dispatch", {"execution_id": "read-execution", "decision_id": "read-decision"}, [{"path": "/receipt/status", "equals": "completed"}])
    denied = dict(action, decision_id="external-denial", grant_id=None, intent={"operation": "external-action", "description": "Unallocated external control"})
    op(r, "external-denial", "agency-check", denied, [{"path": "/status", "equals": "denied"}])
    op(r, "actor-mask", "agency-actor-view", {"view_id": "actor-view", "actor": actor_ref, "model_revision": revision,
        "as_of": now().isoformat(), "clock_mapping_assumption": "UTC host; actor mask authored", "owned_goals": ["Review finding"],
        "attributed_policy": "Research only", "attribution": ATTR})
    op(r, "delivery", "deliver-finding", {"finding_id": "finding"}, [{"path": "/external_message_sent", "equals": False}])
    op(r, "c4-assessment-read", "reason-assessments", {"kind": "comparison", "limit": 10})
    save("finish-complete.json", {"status": "completed-pending-fresh-process-restart", "comparison": comparison["results"],
        "student_revisions": len([j for j in ep.jobs if j.role == "student" and j.status == "completed"]), "teacher_responses": len([j for j in ep.jobs if j.role == "teacher" and j.status == "completed"])})


def restart():
    # No environment key, gateway construction or inference dispatch in this process.
    r = runtime(False)
    checks = {}
    for path in sorted(ROOT.glob("*.workflow.json")):
        name = path.name.removesuffix(".workflow.json")
        state = r.workflow.resume(name)
        original = read(path.name)
        if original["state"] != "completed":
            if state.state != original["state"] or state.error != original["error"]: raise RuntimeError("Retained failure differs: " + name)
            checks[name] = "original failure preserved"
            continue
        if state.state != "completed": raise RuntimeError("Restart workflow differs: " + name)
        if r.workflow.output(name, "handoff") != read(name + ".json"): raise RuntimeError("Restart output differs: " + name)
    checks["workflow_replay"] = "identical outputs, no native redispatch"
    ep = r.reasoning.get("inquiry")
    if plain(ep) != read("reasoning-final.json"): raise RuntimeError("C4 episode differs after restart")
    checks["c4_episode"] = "identical"
    for path in sorted(ROOT.glob("owners*.sqlite3")):
        with sqlite3.connect(path) as db:
            result = db.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok": raise RuntimeError(str(path) + ": " + result)
            checks[path.name] = result
    if len([k for k in checks if k.endswith("sqlite3")]) != 8: raise RuntimeError("Expected eight owner stores")
    save("restart-complete.json", {"status": "completed", "checks": checks, "new_model_calls": 0,
        "limitation": "Normal process restart/replay; no fault injection or crash durability qualification"})


if __name__ == "__main__":
    stage = sys.argv[1]
    try: {"initial": initial, "finish": finish, "restart": restart}[stage]()
    except Exception as error:
        stamp = now().strftime("%Y%m%dT%H%M%S%f")
        save(stage + "-failure-" + stamp + ".json", {"type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc()})
        raise
