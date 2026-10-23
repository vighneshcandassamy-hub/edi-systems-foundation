"""Operator teacher exchange with an embedded native checkpoint at every pause.

This changes checkpoint delivery only. It does not choose student actions,
rewrite frozen cuts, import world evidence, or replay inference.
"""
import hashlib
import json
from pathlib import Path
import runpy
import time


def show_handoff(out, source):
    out, source = Path(out), Path(source)
    state = json.loads((out / "latest-state.json").read_bytes())
    runpy.run_path(str(source / "checkpoint.py"))["display_checkpoint"](out, source)
    print("EDI_HANDOFF_STATE", json.dumps({k: v for k, v in state.items()
        if k not in ("mission", "evidence", "artifact_frontier")}), flush=True)
    if state.get("state") != "waiting-teacher":
        return
    job_id = state["job_id"]
    pending = json.loads((out / "teacher-pending.json").read_bytes())
    if pending["job_id"] != job_id:
        raise RuntimeError("Pending marker and durable state differ; preserve checkpoint before any import")
    path = out / "teacher-exchange" / (hashlib.sha256(job_id.encode()).hexdigest() + ".request.json")
    request = json.loads(path.read_bytes())
    assert request["job"]["job_id"] == job_id
    print(json.dumps(request, separators=(",", ":")), flush=True)


def import_feedback(out, source, job_id, feedback, timeout_seconds=180):
    out, source = Path(out), Path(source)
    assert 1 <= timeout_seconds <= 180
    pending = json.loads((out / "teacher-pending.json").read_bytes())
    state = json.loads((out / "latest-state.json").read_bytes())
    assert state.get("state") == "waiting-teacher" and pending["job_id"] == state["job_id"] == job_id
    payload = json.dumps(feedback, sort_keys=True).encode()
    # Exclusive creation prevents an ambiguous browser retry from dispatching twice.
    with (out / ("teacher-feedback-" + job_id + ".json")).open("xb") as stream:
        stream.write(payload)
    (out / "teacher-feedback.json").write_bytes(payload)
    with (out / ("command-" + str(time.time_ns()) + "-import-teacher.json")).open("x") as stream:
        json.dump({"stage": "import-teacher"}, stream)
    print("EDI_FEEDBACK_QUEUED", job_id, flush=True)
    deadline = time.monotonic() + timeout_seconds
    last_progress = 0
    settled = False
    while time.monotonic() < deadline:
        state = json.loads((out / "latest-state.json").read_bytes())
        receipt = (out / ("teacher-import-" + job_id + ".json")).exists()
        next_teacher = state.get("state") == "waiting-teacher" and state.get("job_id") != job_id
        terminal = (out / "terminal.json").exists() and (out / "restart-complete.json").exists()
        failed = state.get("state") == "waiting-model" or json.loads((out / "autonomous-server.json").read_bytes()).get("stage") == "failed"
        if receipt and (next_teacher or terminal or failed):
            settled = True
            break
        if time.monotonic() - last_progress >= 20:
            print("EDI_WAITING_FOR_NATIVE_PAUSE", state.get("turn"), state.get("state"), flush=True)
            last_progress = time.monotonic()
        time.sleep(2)
    print("EDI_CHECKPOINT_PAUSE", json.dumps({"settled": settled,
        "scope": "Native pause observed" if settled else "Timed out; cross-owner quiescence is not established; do not retry an unknown inference"}), flush=True)
    show_handoff(out, source)
