"""Actual Cedar wiring qualification, with authored proposals and no model calls."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import sys
import uuid
from offline_runner import BoundaryError, wire
from cedar_pair import CedarPair

MODEL = {"id":"authored-connection-fixture", "revision":"1", "reasoning":"no-model"}


def response(packet, proposal):
    return wire({**{k:packet[k] for k in ("arm","request_id","payload_sha256")}, "proposal":proposal}).encode()


def baseline_proposal(name, args):
    return {"rationale":"Authored connection check only", "uncertainty":"No ecological inference",
            "predictions":[], "notes":"Authored connection notes retained alongside action", "operation":{"name":name,"args":args}}


def native_proposal(packet, name, args):
    native = packet["payload"]["native"]
    data = json.loads(native["messages"][1]["content"][0]["text"])
    if name == "yield":
        operation = {"operation":"yield", "arguments":{"reason":"Connection check complete; no scientific investigation authorized by this fixture",
            "assessment":{"disposition":"paused", "unresolved_needs":[],
                "alternatives_considered":[{"operation":"world-call", "reason_for_not_using":"No ecological inquiry or intervention in this connection fixture"}],
                "resume_when":"A fresh independently qualified participant and live launch approval"}}}
    else:
        operation = {"operation":"world-call", "arguments":{"operation":name,"body":args}}
    return {"rationale_summary":"Authored native connection fixture, no model inference",
        "limitation":"Only verifies public dispatch, separation, persistence and termination",
        "decision_basis":{"evidence_record_ids":[x["reference"]["record_id"] for x in data["context"]["evidence"]],
            "understanding":"Connection qualification only", "information_need":"Verify exact native transport",
            "expected_use":"Retain wiring evidence without ecological action"},
        "operation_proposals":[operation]}


def run(source, directory):
    source, directory = Path(source).resolve(), Path(directory).resolve()
    os.environ["EDI_MEADOWS_ROOT"] = str(source/"meadows")
    pair = CedarPair(source, directory, MODEL)
    result = {"scope":"Actual Cedar connection qualification with authored responses; NOT an intelligence comparison",
              "model_calls":0,"paid_calls":0,"scientific_benchmark_started":False}
    try:
        first = {arm:pair.export(arm) for arm in ("baseline","edi")}
        before = {a:w.snapshot() for a,w in pair.worlds.items()}
        for arm in ("baseline","edi"):
            assert pair.export(arm) == first[arm]
        assert before == {a:w.snapshot() for a,w in pair.worlds.items()}
        result["repeat_export_no_world_replay"] = True
        try:pair.evaluate()
        except BoundaryError:pass
        else:raise AssertionError("Premature evaluator was not blocked")
        # Cross-arm identity must not consume the other arm's live pending job.
        for arm, other in (("baseline","edi"),("edi","baseline")):
            try:pair.consume(arm,first[other]["request_id"],response(first[other],{}))
            except BoundaryError:pass
            else:raise AssertionError("Foreign request accepted")
            assert pair.export(arm) == first[arm]
        result["cross_arm_import_blocked_without_pending_mutation"] = True
        # Exercise the public operation path in both independent Cedar brokers.
        for name, args in (("sources",{}),("status",{}),("yield",{"reason":"Connection check only"})):
            for arm in ("baseline","edi"):
                packet = pair.export(arm)
                proposal = baseline_proposal(name,args) if arm == "baseline" else native_proposal(packet,name,args)
                state = pair.consume(arm,packet["request_id"],response(packet,proposal))
                if name != "yield":
                    assert not (state.get("terminal") if arm == "baseline" else state["state"] in ("completed","yielded")), state
            if name != "yield":
                assert pair.worlds["baseline"].snapshot()["state_sha256"] == pair.worlds["edi"].snapshot()["state_sha256"]
        after = {a:w.snapshot() for a,w in pair.worlds.items()}
        assert all([op for _,op in snapshot["events"]] == ["mission","sources","status"] for snapshot in after.values())
        assert after["baseline"]["state_sha256"] == pair.initial_state_sha256
        assert after["edi"]["state_sha256"] == pair.initial_state_sha256
        # Both arms yielded. Exercise the actual operator evaluator only now;
        # its year-zero values are not model intelligence or ecological results.
        evaluated = pair.evaluate()
        assert evaluated["terminal"] == {"baseline":"yielded","edi":"yielded"}
        result.update(passed=True, initial_state_sha256=pair.initial_state_sha256,
            public_operations_each=["mission","sources","status"],
            authored_accepted_proposals_each=3, post_terminal_evaluation_returned=True,
            outcomes_are_zero_year_connection_fixtures=True,
            transport_usage={a:c.usage() for a,c in pair.pair.channels.items()},
            initial_and_final_world_states_identical=True, teacher_enabled=False,
            source_manifest_sha256=sha256((source/"source-manifest.json").read_bytes()).hexdigest())
        integrity = {}
        for p in directory.rglob("*.sqlite*"):
            if p.name.endswith(("-wal","-shm")):continue
            with sqlite3.connect(p) as db:
                integrity[p.relative_to(directory).as_posix()] = db.execute("pragma integrity_check").fetchone()[0]
        assert all(v == "ok" for v in integrity.values())
        assert pair.baseline.state()["notes"] == "Authored connection notes retained alongside action"
        result["inline_baseline_notes_verified"] = True
        result["integrity"] = integrity
        pair._save("connection-result.json",result)
        return result
    finally:
        pair.close()


if __name__ == "__main__":
    print("CEDAR_PAIR_CONNECTION_RESULT", json.dumps(run(sys.argv[1],sys.argv[2])),flush=True)
