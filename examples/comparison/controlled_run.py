"""Explicit, serial paired comparison. Default policy forbids any network inference.

Call only on Kaggle with an authorized fixed policy and explicit transport.
No command-line main, implicit key lookup, background polling or automatic rerun.
"""
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import secrets
from offline_runner import BoundaryError, Limits, wire
from cedar_pair import CedarPair
from responses_adapter import BudgetedResponses, SpendPolicy, request_body

MODEL = {"id":"gpt-6.1-sol","revision":"api-alias-20261027","reasoning":"low"}
METRICS = ("years_elapsed","mean_damage_fraction","total_operational_spending",
           "total_timber_delivery","five_year_committed_delivery_shortfall",
           "broad_treatment_dose_sum","terminal_mean_foliage","terminal_mean_enemy_index")


def validate_launch(policy, approval, post):
    if not policy.approved_by_user:
        raise BoundaryError("No paid inference authorization; no world or provider started")
    if asdict(policy) != asdict(SpendPolicy(approved_by_user=True)):
        raise BoundaryError("Only the reviewed $20 local reservation policy may launch")
    expected={"financial_authorization":True,"restricted_api_access_authorized":True,
              "provider_hard_limit_verified":True,"auto_recharge_disabled_verified":True,
              "local_reservation_usd":20,"model":MODEL["id"]}
    if not isinstance(approval,dict) or any(approval.get(k)!=v for k,v in expected.items()):
        raise BoundaryError("Explicit approval and verified provider controls required")
    if not isinstance(approval.get("confirmed_at"),str) or not approval["confirmed_at"].strip():
        raise BoundaryError("Contemporaneous approval receipt required")
    if not callable(post):raise BoundaryError("Explicit isolated provider transport required")


def write_comparison(directory, evaluation, usage):
    """Mechanical results only; participant hypotheses remain verbatim, labelled."""
    directory=Path(directory)
    document={"status":"paired_run_terminated","evaluation":evaluation,"provider_usage":usage,
        "limits":{"replications":1,"model_snapshot":"Mutable API alias; no dated snapshot published",
                  "identity":"Same model/config in both arms; exact Work Mode backend identity unverified",
                  "isolation":"Explicit stateless requests only; no ChatGPT memory/conversation identifiers",
                  "validity":"One constructed Cedar pair; no general superiority, significance or energy claim"}}
    (directory/"comparison.json").write_text(json.dumps(document,indent=2,allow_nan=False))
    lines=["# Controlled Cedar comparison", "", "One independently initialized world per arm. This is one constructed case, not a general superiority test.","",
           "| Outcome | Model only | Model + EDI |","|---|---:|---:|"]
    outcomes=evaluation["outcome"]
    for key in METRICS:
        lines.append("| "+key+" | "+str(outcomes["baseline"].get(key,"not reported"))+" | "+str(outcomes["edi"].get(key,"not reported"))+" |")
    for arm,label in (("baseline","Model only"),("edi","Model + EDI")):
        final=outcomes[arm].get("final_report")
        lines.extend(["", "## "+label+" participant report", "", "Terminal disposition: "+evaluation["terminal"][arm]+".",""])
        if final:
            report=final.get("conclusion",wire(final)) if isinstance(final,dict) else str(final)
            (directory/(arm+"-participant-report.md")).write_text(report)
            lines.extend(["The following is the participant's submitted explanation, not independent causal validation.","",report])
        else:lines.append("No accepted final report. The arm did not finish the mission; retained proposals and receipts remain in its ledger.")
    lines.extend(["","## Interpretation limits","",
        "Compare the reported outcome vector, accepted final reports, prospective hypotheses/tests and actual measured usage together. No composite score was invented. A cheaper or more complete arm is not automatically causally better; constraint violations and untested mechanisms must remain visible.","",
        "Only explicit current-arm data was sent in each model request, with no previous_response_id, conversation, external tools or remote files. This controls the client request, not unobservable provider internals or pretraining familiarity. The mutable alias and one case limit reproducibility and generalization.","",
        "Provider usage and spending reservations are in comparison.json and provider.sqlite3. Local reservations bound planned generation exposure, not exact invoices; provider hard-limit enforcement can lag. Energy was not measured."])
    (directory/"comparison.md").write_text("\n".join(lines))
    return document


def run(source, directory, *, policy=SpendPolicy(), approval=None, post=None):
    validate_launch(policy,approval,post)  # Before importing a world or opening a provider connection.
    source,directory=Path(source).resolve(),Path(directory).resolve()
    if directory.exists():raise BoundaryError("Fresh directory required; never restart a previous run")
    os.environ["EDI_MEADOWS_ROOT"]=str(source/"meadows")
    pair=None;client=None
    try:
        pair=CedarPair(source,directory,MODEL,Limits())
        client=BudgetedResponses(directory/"provider.sqlite3",policy,post=post)
        order=["baseline","edi"]
        if secrets.randbelow(2):order.reverse()
        manifest={"created_at":datetime.now(timezone.utc).isoformat(),"model":MODEL,
            "policy":asdict(policy),"limits":asdict(Limits()),"initial_order":order,
            "approval":approval,"initial_state_sha256":pair.initial_state_sha256,
            "source_manifest_sha256":sha256((source/"source-manifest.json").read_bytes()).hexdigest(),"instructions":"No prior Cedar answer, evaluator output or other-arm data enters requests"}
        (directory/"launch.json").write_text(json.dumps(manifest,indent=2,allow_nan=False))
        # Qualify BOTH initial prompt shapes before the first generation. These
        # authenticated count calls are retained and never described as free.
        counts={}
        for arm in order:
            packet=pair.export(arm)
            counted=client.prepare(packet)
            counts[arm]=counted
            (directory/"initial-prompt-counts.json").write_text(json.dumps(counts,indent=2))
            n=counted.get("input_tokens")
            if counted.get("object")!="response.input_tokens" or type(n) is not int or not 0<=n<=policy.max_input_tokens:
                raise BoundaryError("An initial prompt exceeds the fixed cap or count is unknown; neither arm generated")
        while True:
            terminal=dict(pair.pair.db.execute("SELECT arm,state FROM terminal"))
            if len(terminal)==2:break
            for arm in order:
                if arm in terminal:continue
                try:packet=pair.export(arm)
                except BoundaryError:
                    channel=pair.pair.channels[arm]
                    count=channel.db.execute("SELECT count(*) FROM calls").fetchone()[0]
                    budget=(count>=channel.limits.max_calls or (count+1)*16384>channel.limits.max_reserved_tokens
                            or channel.age()>channel.limits.max_seconds
                            or (arm=="baseline" and pair.baseline.state()["decisions"]>=channel.limits.max_decisions))
                    if not budget:raise
                    pair.pair.mark_terminal(arm,"yielded")
                    continue
                raw=client.complete(packet)
                try:pair.consume(arm,packet["request_id"],raw)
                except BoundaryError:
                    # Baseline protocol correction is limited by its own durable
                    # validator. Unknown action/transport outcomes never retry.
                    state=pair.baseline.state() if arm=="baseline" else None
                    if state is None or state["terminal"]=="blocked-unknown-action":raise
                    if state["terminal"]:pair.pair.mark_terminal(arm,"yielded")
                    elif state["corrections"]!=1:raise
                (directory/"provider-progress.json").write_text(json.dumps(client.summary(),indent=2))
        evaluation=pair.evaluate()  # First private evaluation; both arms terminal.
        return write_comparison(directory,evaluation,client.summary())
    except Exception as exc:
        if directory.exists():
            # Never serialize credentials or arbitrary provider exception bodies.
            (directory/"blocked.json").write_text(json.dumps({"exception_type":type(exc).__name__,
                "reason":str(exc)[:500] if isinstance(exc,BoundaryError) else "Retained native/provider artifacts require reconciliation",
                "automatic_retry":False,"comparison_complete":False},indent=2))
        raise
    finally:
        if pair is not None:pair.close()
        if client is not None:client.db.close()
