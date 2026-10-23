"""Reopen native controller state with dispatch-forbidden ports; no service restart."""
import argparse
import json
import os
from pathlib import Path
import sqlite3
from types import SimpleNamespace

from edi.inquiry.application import ApplicationProfile
from edi.inquiry.benchmark import Investigation
from edi.inquiry.runtime import Runtime
from edi.reason.config import ReasoningProfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.run_root.resolve()
    profile = ApplicationProfile.load(root / "application.json")
    os.environ["EDI_AUTONOMOUS_ROOT"] = str(root)
    os.environ["EDI_AUTONOMOUS_RUN_ID"] = profile.run_id
    os.environ["EDI_AUTONOMOUS_WORKSPACE"] = profile.application_id
    from run import snapshot, snapshot_differences

    class ForbiddenPort:
        def __init__(self, binding=None, session_id=None):
            self.binding, self.session_id = binding, session_id
        def complete(self, *args, **kwargs):
            raise AssertionError("Offline restart must never dispatch inference")
        def call(self, *args, **kwargs):
            raise AssertionError("Offline restart must never contact the broker")

    reason = profile.reasoning or ReasoningProfile(workspace_id=profile.observation.workspace_id,
        database=profile.observation.database.with_name(profile.observation.database.stem + ".reason.sqlite3"),
        student=profile.student.binding, teacher=profile.teacher.binding)
    runtime = Runtime(profile.observation, profile.world, profile.interpretation, reason,
        profile.analysis, profile.assessment, profile.agency, profile.workflow)
    runtime.interpretation
    runtime.analysis
    runtime.assessment
    investigation = Investigation(runtime, ForbiddenPort(session_id=profile.broker.grant.session_id),
        ForbiddenPort(binding=profile.student.binding), runtime.workflow.profile.database,
        profile.run_id, teacher_gateway=None if profile.teacher.mode == "disabled" else ForbiddenPort(binding=profile.teacher.binding),
        max_turns=profile.max_turns, max_tokens=profile.max_tokens,
        session_seconds=profile.session_seconds, max_corrections=profile.max_corrections,
        teaching_mode=profile.teaching_mode, use_teaching_memory=profile.use_teaching_memory,
        input_token_cap=min(16384, profile.student.max_model_len - 4096))
    baseline = json.loads((root / "restart-baseline.json").read_bytes())
    observed = snapshot(SimpleNamespace(runtime=runtime, investigation=investigation))
    differences = snapshot_differences(baseline, observed)
    integrity = {}
    for path in sorted(root.glob("*.sqlite3")):
        with sqlite3.connect(path) as db:
            integrity[path.name] = db.execute("PRAGMA integrity_check").fetchone()[0]
    report = {"scope": "fresh-process native controller reopen with dispatch-forbidden ports; model/broker service restart and crash recovery unqualified",
        "same_native_snapshot": not differences, "differences": differences,
        "new_model_dispatches": 0, "new_broker_requests": 0, "integrity": integrity,
        "controller_state": observed["state"], "passed": not differences and len(integrity) == 8 and set(integrity.values()) == {"ok"}}
    path = root / "offline-restart-audit.json"
    assert not path.exists(), "Keep the original restart result"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    assert report["passed"], "Inspect retained restart differences/integrity"


if __name__ == "__main__":
    main()
