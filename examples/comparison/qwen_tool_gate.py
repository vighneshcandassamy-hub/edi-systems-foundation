"""Actual-model generic discovery/read/recovery/report qualification, no Cedar.

Synthetic inventory task. All model responses/usages retained. These calls are
qualification overhead, not participant-arm performance or ecological evidence.
"""
import json
from local_qwen_adapter import MODEL,BASE_SCHEMA,COMMON,strict
from public_protocol import bind_schema,GUIDANCE
from offline_runner import BoundaryError,wire

def qualify(post,root):
    view={"version":"synthetic-public-tool-binding/1.0","decision":0,"remaining_decisions":8,
          "public_year":0,"documents":{},"acquired_document_ids":[],"people":{},"sources":{},"stand_ids":[],
          "public_event_count":0,"public_attempt_count":0,"blocked_operations_at_this_cut":[],"recent_failures":[],"last_public_receipt":None}
    history=[];calls=[];read=False;recovered=False;closed=False
    task=("Neutral warehouse exercise, unrelated to Cedar. Investigate why recorded widget inventory differs from the audit. "
          "Discover and read the public inventory document, then submit a report identifying the discrepancy, recommendation "
          "and uncertainty. Public discovery/read/status/submit are available. No experiment or time advance is needed. "
          "A source ID S-archive and internal evidence record R-note are not document IDs. Do not guess a public ID.")
    for turn in range(8):
        schema=bind_schema(BASE_SCHEMA,"baseline",view)
        messages=[{"role":"system","content":COMMON+" "+GUIDANCE},
                  {"role":"user","content":wire({"task":task,"public_bindings":view,"history":history})}]
        counted=strict(post("/tokenize",{"model":MODEL["id"],"messages":messages,"add_generation_prompt":True}))
        body={"model":MODEL["id"],"messages":messages,"max_tokens":1024,"temperature":0,"seed":17,
              "response_format":{"type":"json_schema","json_schema":{"name":"neutral_tool_use","strict":True,"schema":schema}}}
        raw=post("/v1/chat/completions",body);obj=strict(raw)
        (root/("tool-gate-call-%02d.json"%turn)).write_bytes(raw)
        choice=obj["choices"][0];proposal=strict(choice["message"]["content"]);usage=obj["usage"]
        if obj["model"]!=MODEL["id"] or choice["finish_reason"]!="stop" or usage["prompt_tokens"]!=counted["count"]:
            raise BoundaryError("Actual tool qualification model/context/usage failed")
        calls.append(usage);op=proposal["operation"];name,args=op["name"],op["args"]
        if name=="search":
            doc="D-inventory-v2" if recovered else "D-inventory"
            view["documents"]={doc:"Inventory and audit record"}
            result={"http_status":200,"body":{"items":[{"id":doc,"title":"Inventory and audit record"}]}}
        elif name=="read" and args.get("document_id") in view["documents"]:
            if not recovered:
                # A definite, deliberately injected stale-catalogue response.
                result={"http_status":404,"body":{"code":"not_found","message":"D-inventory was superseded. Search the catalogue again; do not repeat this read."}}
                view["documents"]={};view["blocked_operations_at_this_cut"]=["read"]
                view["recent_failures"]=[{"intent":op,"http_status":404}]
                recovered=True
            else:
                result={"http_status":200,"body":{"id":"D-inventory-v2","body":"Recorded widgets: 10. Audited widgets: 8. Two recorded receipts have no signed delivery proof. Audit may have missed a storage location."}}
                view["acquired_document_ids"]=["D-inventory-v2"];read=True
        elif name=="submit" and read:
            report=args.get("conclusion","")
            if len(report)<100 or "2" not in report and "two" not in report.lower():
                raise BoundaryError("Actual generic report failed evidence/content criterion")
            result={"http_status":200,"body":{"status":"accepted"}};closed=True
        elif name in ("sources","people","status","mission"):
            result={"http_status":200,"body":{"note":"Use search to discover the inventory document."}}
        else:
            result={"http_status":422,"body":{"message":"Not applicable to this neutral task; discover and read the record before submitting."}}
        history.append({"proposal":proposal,"receipt":result});view["last_public_receipt"]=result
        view["decision"]=turn+1;view["remaining_decisions"]=7-turn
        if result["http_status"]==200:view["blocked_operations_at_this_cut"]=[]
        (root/"neutral-tool-gate.json").write_text(json.dumps({"passed":closed,"synthetic":True,"cedar_world_started":False,
            "read":read,"definite_error_recovery":recovered,"calls":calls,"history":history},indent=2),encoding="utf-8")
        print("QWEN_TOOL_GATE",turn+1,name,result["http_status"],flush=True)
        if closed:return
    raise BoundaryError("Actual model did not complete generic discovery/read/error-recovery/report gate in eight calls")
