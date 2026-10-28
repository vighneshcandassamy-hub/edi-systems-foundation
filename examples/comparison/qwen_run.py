"""Explicit fresh Kaggle Qwen comparison. Never auto-starts at import.
Requires reviewed source, a qualified local serving receipt and explicit approval.
"""
from datetime import datetime,timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import secrets
from offline_runner import BoundaryError,Limits,wire
from cedar_pair import CedarPair
from local_qwen_adapter import MODEL,LocalQwen,Loopback

METRICS=("years_elapsed","mean_damage_fraction","total_operational_spending",
         "total_timber_delivery","five_year_committed_delivery_shortfall",
         "broad_treatment_dose_sum","terminal_mean_foliage","terminal_mean_enemy_index")

def validate(approval,receipt):
    expected={"authorized":True,"kaggle_only":True,"paid_services":False,
              "model":MODEL,"neutral_checks_passed":True,"local_model_smoke_passed":True}
    if not isinstance(approval,dict) or any(approval.get(k)!=v for k,v in expected.items()):
        raise BoundaryError("Explicit Kaggle authorization and completed qualification receipts required")
    if not isinstance(receipt,dict) or receipt.get("model")!=MODEL:
        raise BoundaryError("Pinned local model receipt missing")
    if receipt.get("max_model_len")!=16384 or receipt.get("teacher_enabled") is not False:
        raise BoundaryError("Serving context/teacher settings differ")
    if (not receipt.get("weight_files_sha256") or not receipt.get("tokenizer_files_sha256")
        or not receipt.get("vllm_version") or not receipt.get("gpu_inventory")):
        raise BoundaryError("Weight/tokenizer/package/GPU evidence missing")
    if receipt.get("vision_preprocessor_cache_gb")!=0:
        raise BoundaryError("Disable cross-request vision preprocessor caching")
    if receipt.get("prefix_caching_enabled") is not False:
        raise BoundaryError("Disable cross-request prefix caching for measured comparison")

def write_result(directory,evaluation,usage):
    document={"status":"paired_run_terminated","model":MODEL,"evaluation":evaluation,"local_model_usage":usage,
              "scope":"One fresh constructed Cedar pair; no general superiority or energy claim"}
    directory=Path(directory)
    (directory/"comparison.json").write_text(json.dumps(document,indent=2,allow_nan=False),encoding="utf-8")
    lines=["# Qwen alone versus Qwen with native EDI","","One fixed local model; one independently initialized world per arm.","",
           "| Outcome | Qwen alone | Qwen + EDI |","|---|---:|---:|"]
    for metric in METRICS:
        lines.append("| "+metric+" | "+str(evaluation["outcome"]["baseline"].get(metric))+" | "+str(evaluation["outcome"]["edi"].get(metric))+" |")
    for arm in ("baseline","edi"):
        final=evaluation["outcome"][arm].get("final_report")
        lines.extend(["","## "+arm+" participant report",""])
        if final:
            report=final.get("conclusion",wire(final)) if isinstance(final,dict) else str(final)
            (directory/(arm+"-participant-report.md")).write_text(report,encoding="utf-8")
            lines.extend(["Participant explanation; not independent causal validation.","",report])
        else:lines.append("No accepted participant report; retain this failure, do not invent one.")
    lines.extend(["","## Limits","","Both arms were terminal before private evaluation. Prior Cedar answers were excluded from requests. "
                  "Current-arm stateless model calls, retained native receipts and measured usage support a case-specific comparison. "
                  "One pair cannot establish general superiority or significance. Energy is unknown."])
    (directory/"comparison.md").write_text("\n".join(lines),encoding="utf-8")
    return document

def run(source,directory,*,endpoint,serving_token,approval=None,serving_receipt=None,post=None):
    validate(approval,serving_receipt)
    if not Path("/kaggle/working").is_dir():
        raise BoundaryError("Actual execution is restricted to Kaggle")
    source,directory=Path(source).resolve(),Path(directory).resolve()
    if directory.exists():raise BoundaryError("Fresh pair directory required")
    os.environ["EDI_MEADOWS_ROOT"]=str(source/"meadows")
    client=None;pair=None
    try:
        directory.mkdir(parents=True,exist_ok=False)
        # Separate provider ledger from the new pair directory, whose owner
        # requires exclusive creation. No world starts during client construction.
        client=LocalQwen(directory/"local-model.sqlite3",post=post or Loopback(endpoint,serving_token))
        pair=CedarPair(source,directory/"pair",MODEL,Limits(),
                       native_request_token_counter=client.count_native_request)
        order=["baseline","edi"]
        if secrets.randbelow(2):order.reverse()
        launch={"created_at":datetime.now(timezone.utc).isoformat(),"model":MODEL,
                "limits":Limits().__dict__,"initial_order":order,
                "source_manifest_sha256":sha256((source/"source-manifest.json").read_bytes()).hexdigest(),
                "initial_state_sha256":pair.initial_state_sha256,"serving_receipt":serving_receipt,
                "qualification":approval,
                "prior_case_solution_supplied":False}
        (directory/"launch.json").write_text(json.dumps(launch,indent=2),encoding="utf-8")
        counts={}
        for arm in order:
            packet=pair.export(arm)
            counts[arm]=client.prepare(packet)
        (directory/"initial-counts.json").write_text(json.dumps(counts,indent=2),encoding="utf-8")
        while True:
            terminal=dict(pair.pair.db.execute("SELECT arm,state FROM terminal"))
            if len(terminal)==2:break
            for arm in order:
                if arm in terminal:continue
                packet=pair.export(arm) # Capacity expiry blocks; never invent a terminal receipt.
                raw=client.complete(packet)
                try:pair.consume(arm,packet["request_id"],raw)
                except BoundaryError:
                    if arm!="baseline":raise
                    state=pair.baseline.state()
                    if state["terminal"]=="blocked-unknown-action":raise
                    if state["terminal"]:pair.pair.mark_terminal(arm,"yielded")
                    elif state["corrections"]!=1:raise
                (directory/"progress.json").write_text(json.dumps(client.summary(),indent=2),encoding="utf-8")
        evaluated=pair.evaluate()
        return write_result(directory,evaluated,client.summary())
    except Exception as exc:
        if directory.exists():
            (directory/"blocked.json").write_text(json.dumps({
                "exception_type":type(exc).__name__,
                "reason":str(exc)[:500] if isinstance(exc,BoundaryError) else "Native artifacts require reconciliation",
                "comparison_complete":False,"automatic_retry":False},indent=2),encoding="utf-8")
        raise
    finally:
        if pair is not None:pair.close()
        if client is not None:client.db.close()
