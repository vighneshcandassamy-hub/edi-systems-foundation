"""Drive only IntegratedApplication.step; no authored component sequence.

Each process advances at most one native controller turn. The supervisor owns
process scheduling, not operation choice. Persisted inputs are never rewritten.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import traceback

from edi.inquiry.application import ApplicationProfile, IntegratedApplication
from edi.shared.durable_io import canonical, digest
from edi.shared.errors import EDIError, ErrorCode
from neutral_world import MISSION

OUT = Path(os.environ.get("EDI_AUTONOMOUS_ROOT", "/kaggle/working/edi-autonomous-20261023"))
REV = "0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
WORKSPACE = os.environ.get("EDI_AUTONOMOUS_WORKSPACE", "autonomous-20261023")
RUN = os.environ.get("EDI_AUTONOMOUS_RUN_ID", "neutral-controller")


def save(name, value):
    path = OUT / name
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if path.exists():
        assert path.read_bytes() == raw, "immutable artifact changed: " + name
    else:
        path.write_bytes(raw)


def configuration():
    path = OUT / "application.json"
    if path.exists():
        return ApplicationProfile.load(path)
    now = datetime.now(timezone.utc)
    binding = {"model_id": "Qwen/Qwen3-VL-8B-Instruct", "revision": REV, "provider": "local-vllm", "engine": "vllm/0.21.0", "tokenizer_revision": REV}
    teacher = {"model_id": "ChatGPT-current-session-operator-declared", "revision": "autonomous-critique-20261023", "provider": "manual-file-exchange", "engine": "current-assistant-session-unverified", "tokenizer_revision": "unmeasured"}
    config = {"application_id": WORKSPACE, "run_id": RUN,
        "observation": {"workspace_id": WORKSPACE, "database": str(OUT / "owners.sqlite3")},
        "student": {"binding": binding, "max_images": 0, "completion_timeout_seconds": 600},
        "teacher": {"binding": teacher, "directory": str(OUT / "teacher-exchange"), "attribution": "Current ChatGPT assistant; operator-declared identity; implementation context known; critique only"},
        "agency": {"workspace_id": WORKSPACE, "database": str(OUT / "owners.agency.sqlite3"), "operator_ids": ["engineering-operator"]},
        "broker": {"grant": {"grant_id": WORKSPACE, "session_id": WORKSPACE, "workspace_id": WORKSPACE, "endpoint": "http://127.0.0.1:8098", "token_sha256": hashlib.sha256(os.environ["EDI_BROKER_TOKEN"].encode()).hexdigest(), "mission_sha256": digest(MISSION), "operator_id": "engineering-operator", "not_before": (now - timedelta(seconds=1)).isoformat(), "expires_at": (now + timedelta(hours=2)).isoformat(), "operations": list(MISSION["public_operations"]), "maximum_requests": 64}},
        "max_turns": 24, "max_tokens": 393216, "session_seconds": 3600, "max_corrections": 1}
    profile = ApplicationProfile.model_validate_json(json.dumps(config))
    save("application.json", profile.model_dump(mode="json"))
    return ApplicationProfile.load(path)


def snapshot(app):
    state = app.investigation.state()
    episodes = []
    count = state.get("pending_turn", state["turn"])
    for index in range(count + 1):
        try:
            ep = app.runtime.reasoning.get(RUN + ":inquiry:" + str(index))
        except EDIError as exc:
            if index == count and exc.code == ErrorCode.NOT_FOUND:
                break
            raise
        episodes.append(ep.model_dump(mode="json"))
    ledger = json.loads((OUT / "world-session.json").read_bytes())
    # Gateway table names are owner-defined; snapshot all IO counters for audit.
    counters = {}
    with sqlite3.connect(app.runtime.reasoning.profile.database) as db:
        for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'io_%'").fetchall():
            counters[table] = list(db.execute('SELECT count(*),coalesce(sum(attempts),0) FROM "' + table + '"').fetchone())
    return {"state": state, "episodes": episodes, "broker_requests": len(ledger["requests"]), "conclusions": ledger["conclusions"], "c4_io_counters": counters}


def snapshot_differences(expected, actual, path="$"):
    if type(expected) != type(actual):
        return [{"path": path, "kind": "type", "expected": type(expected).__name__, "actual": type(actual).__name__}]
    if isinstance(expected, dict):
        result = []
        for key in sorted(set(expected) | set(actual)):
            if key not in expected or key not in actual:
                result.append({"path": path + "." + key, "kind": "missing-key"})
            else:
                result.extend(snapshot_differences(expected[key], actual[key], path + "." + key))
        return result
    if isinstance(expected, list):
        if len(expected) != len(actual): return [{"path": path, "kind": "length", "expected": len(expected), "actual": len(actual)}]
        return [item for i, (left, right) in enumerate(zip(expected, actual)) for item in snapshot_differences(left, right, path + "[" + str(i) + "]")]
    return [] if expected == actual else [{"path": path, "kind": "value", "expected": str(expected)[:256], "actual": str(actual)[:256]}]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    app = IntegratedApplication(configuration())
    # Preflight construction opens every existing owner; no business operation,
    # model, representation admission or investigation sequence is supplied.
    app.runtime.interpretation
    app.runtime.analysis
    app.runtime.assessment
    mode = sys.argv[1]
    before = snapshot(app)
    if mode == "restart":
        baseline = json.loads((OUT / "restart-baseline.json").read_bytes())
        save("restart-observed.json", before)
        differences = snapshot_differences(baseline, before)
        save("restart-mismatch.json", {"differences": differences, "same": not differences})
        integrity = {}
        for path in sorted(OUT.glob("*.sqlite3")):
            with sqlite3.connect(path) as db:
                integrity[path.name] = db.execute("PRAGMA integrity_check").fetchone()[0]
        save("restart-integrity.json", integrity)
        assert not differences, "fresh-process native snapshot changed; inspect restart-mismatch.json"
        assert len(integrity) == 8 and set(integrity.values()) == {"ok"}
        save("restart-complete.json", {"same_native_snapshot": True, "new_model_dispatches": 0, "new_broker_requests": 0, "integrity": integrity, "state": before["state"]})
        print("RESTART_VERIFIED", flush=True)
        return
    if mode == "import-teacher":
        pending = json.loads((OUT / "teacher-pending.json").read_bytes())
        result = app.import_teacher(pending["job_id"], OUT / "teacher-feedback.json")
        save("teacher-import-" + pending["job_id"] + ".json", result)
        print("TEACHER_IMPORTED", flush=True)
        return
    assert mode == "turn"
    baseline_path = OUT / "continuation-baseline.json"
    if baseline_path.exists():
        expected = json.loads(baseline_path.read_bytes())
        # Teacher import deliberately changes its journal; all ordinary ready
        # turn boundaries must reopen without any native or network change.
        if expected["state"]["state"] == "ready":
            assert before == expected, "fresh-process continuation changed prior native state"
    index = before["state"].get("pending_turn", before["state"]["turn"])
    started = datetime.now(timezone.utc)
    current = app.step()
    after = snapshot(app)
    baseline_path.write_text(json.dumps(after, indent=2), encoding="utf-8")
    attempt = len(list(OUT.glob("turn-*-result.json")))
    save(f"turn-{index:02d}-attempt-{attempt:02d}-result.json", {"started_at": started.isoformat(), "completed_at": datetime.now(timezone.utc).isoformat(), "returned_state": current, "snapshot": after})
    (OUT / "latest-state.json").write_text(json.dumps(current, indent=2), encoding="utf-8")
    if current["state"] == "waiting-teacher":
        save("teacher-pending-" + current["job_id"] + ".json", current)
        (OUT / "teacher-pending.json").write_text(json.dumps(current, indent=2), encoding="utf-8")
    elif current["state"] not in ("ready", "in-progress", "waiting-model", "uncertain-completion"):
        save("restart-baseline.json", after)
        save("terminal.json", {"returned_state": current, "snapshot": after, "forest_benchmark_started": False, "scheduling": "real Investigation.step; no authored operation sequence", "teacher_trigger": "student-selected only; optional", "paid_fallback": False})
    print(json.dumps({"turn": index, "state": current["state"], "stop_reason": current.get("stop_reason"), "broker_requests": after["broker_requests"], "c4_io_counters": after["c4_io_counters"]}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        traceback.print_exc()
        OUT.mkdir(parents=True, exist_ok=True)
        name = "process-failure-" + datetime.now(timezone.utc).strftime("%H%M%S%f") + ".json"
        save(name, {"error_type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc(), "no_automatic_inference_retry": True})
        raise
