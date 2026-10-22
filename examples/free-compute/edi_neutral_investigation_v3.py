"""Real C0/C1/C2/C3/C4/C7 loop on a small authored instrument, never the forest."""
from datetime import timedelta
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import base64
from pathlib import Path
import secrets
from threading import Thread
from time import monotonic
import traceback

from edi.agency.benchmark import SimulationGrant
from edi.agency.config import AgencyProfile
from edi.inquiry.benchmark import Investigation
from edi.inquiry.contracts import WorkflowProfile
from edi.inquiry.runtime import Runtime
from edi.observe.benchmark import BrokerConnector
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import ModelBinding
from edi.reason.gateway import NativeGateway, VllmBackend
from edi.shared.config import LocalProfile
from edi.shared.contracts import utc_now
from edi.shared.durable_io import canonical, digest

MODEL="Qwen/Qwen3-VL-8B-Instruct"
REVISION="0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
MISSION={
 "objective":"Use the available instrument records to report what changed, what can be inferred, and what remains uncertain. Obtain information as needed and submit a report.",
 "scope":"Authored neutral engineering instrument only; not empirical science or a forest case.",
 "public_operations":{
  "mission":{"body":{},"returns":"original mission"},
  "sources":{"body":{},"returns":"available document identifiers and descriptions"},
  "read":{"body":{"document_id":"an acquired document identifier"},"returns":"document content"},
  "submit":{"body":{"conclusion":"your report and limitations"},"returns":"closure receipt"}},
 "proposal_protocol":'Request a public operation as {"operation":"world-call","arguments":{"operation":"a public operation name","body":{}}}. Put operation-specific arguments inside body. C0 assigns request_id. You may choose an operation or yield with your reason; the operator supplies no investigation sequence.'
}


def run(endpoint, api_key, out):
 out=Path(out);state=out/"edi-native-loop3-state";state.mkdir(exist_ok=False)
 requests=[];completed_requests={};closed=[];calls=[]
 broker_token=secrets.token_urlsafe(32)
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args): pass
  def do_POST(self):
   if self.headers.get("Authorization")!="Bearer "+broker_token:
    status,answer=401,{"error":"unauthorized"}
   else:
    length=int(self.headers.get("Content-Length","0"))
    if not 0<length<=131072:
     status,answer=422,{"error":"body size"}
    else:
     body=json.loads(self.rfile.read(length));op=self.path.removeprefix("/v2/")
     rid=body.get("request_id");fingerprint=digest([op,body])
     if rid in completed_requests:
      previous=completed_requests[rid]
      status,answer=(previous["status"],previous["answer"]) if previous["fingerprint"]==fingerprint else (409,{"error":"identity conflict"})
     else:
      if closed: status,answer=409,{"error":"session closed"}
      elif op=="mission" and set(body)=={"request_id"}: status,answer=200,{"mission":MISSION}
      elif op=="sources" and set(body)=={"request_id"}:
       status,answer=200,{"items":[{"id":"instrument-log","format":"csv","description":"Recorded instrument samples; acquisition context is contained in the document."}]}
      elif op=="read" and body.get("document_id")=="instrument-log" and set(body)<={"request_id","document_id","include_asset","asset_offset","asset_limit"}:
       content=b"sample,count\n0,8\n1,12\n2,16\n"
       status,answer=200,{"document_id":"instrument-log","format":"csv","source":"simulation",
        "sha256":sha256(content).hexdigest(),"content":content.decode(),
        "source_note":"Authored fixture values. The cause and future behavior are not supplied by these three samples."}
       if body.get("include_asset"):
        offset=body.get("asset_offset",0);limit=body.get("asset_limit",65536)
        if type(offset) is not int or type(limit) is not int or not 0<=offset<=len(content) or not 1<=limit<=65536:
         status,answer=422,{"error":"invalid asset range"}
        else:
         part=content[offset:offset+limit]
         answer["asset"]={"encoding":"base64","offset":offset,"total_bytes":len(content),
          "data":base64.b64encode(part).decode(),"has_more":offset+len(part)<len(content)}
      elif op=="submit" and set(body)=={"request_id","conclusion"} and isinstance(body["conclusion"],str) and body["conclusion"]:
       closed.append(body["conclusion"]);status,answer=200,{"status":"closed","conclusion_received":True}
      else: status,answer=422,{"error":"unsupported operation or arguments","public_operations":MISSION["public_operations"]}
      completed_requests[rid]={"fingerprint":fingerprint,"status":status,"answer":answer}
     requests.append({"operation":op,"body":body,"http_status":status,"response":answer})
   raw=canonical(answer).encode();self.send_response(status)
   self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
 thread=Thread(target=server.serve_forever,daemon=True);thread.start()
 broker_endpoint="http://127.0.0.1:"+str(server.server_port)
 workspace="native-neutral-loop-v3"
 binding=ModelBinding(model_id=MODEL,revision=REVISION,provider="local-kaggle",engine="vllm/0.21.0",tokenizer_revision=REVISION)
 profile=LocalProfile(database=state/"c1.sqlite",workspace_id=workspace)
 rp=ReasoningProfile(database=state/"c4.sqlite",workspace_id=workspace,student=binding)
 ap=AgencyProfile(database=state/"c7.sqlite",workspace_id=workspace)
 wp=WorkflowProfile(database=state/"c0.sqlite",workspace_id=workspace)
 runtime=Runtime(profile,reasoning_profile=rp,agency_profile=ap,workflow_profile=wp)
 grant=SimulationGrant(grant_id=workspace,session_id=workspace,workspace_id=workspace,
  endpoint=broker_endpoint,token_sha256=sha256(broker_token.encode()).hexdigest(),
  mission_sha256=digest(MISSION),operator_id="owner-authorized-neutral-test",
  not_before=utc_now()-timedelta(seconds=1),expires_at=utc_now()+timedelta(minutes=20),
  operations=tuple(MISSION["public_operations"]),maximum_requests=8)
 authority=runtime.agency.benchmark_authority(grant,endpoint=broker_endpoint,
  token_sha256=sha256(broker_token.encode()).hexdigest(),workspace_id=workspace,session_id=workspace)
 connector=BrokerConnector(runtime,broker_endpoint,broker_token,workspace,authority,wp.database,max_requests=8)
 backend=VllmBackend(endpoint,MODEL,api_key=api_key,max_model_len=16384)
 def send(messages,job):
  started=monotonic()
  try: result=backend(messages,job)
  except Exception:
   calls.append({"job_id":job.job_id,"input_tokens":None,"output_tokens":None,"status":"unresolved-provider-call"});raise
  calls.append({"job_id":job.job_id,"input_tokens":result[2],"output_tokens":result[3],"elapsed_seconds":monotonic()-started})
  return result
 gateway=NativeGateway(runtime,binding,rp.database,send,backend.count_tokens,
  attribution="REAL QWEN; public authored neutral instrument; no forest/evaluator data",max_calls=4,max_images=1)
 investigation=Investigation(runtime,connector,gateway,wp.database,"native-neutral-loop3",
  max_turns=4,max_tokens=65536,session_seconds=600)
 report={"kind":"real-C0-neutral-loop","forest_benchmark_started":False,"teacher_enabled":False,
  "max_turns":4,"max_tokens":65536,"mission":MISSION,"model":binding.model_dump(mode="json"),
  "turns":[],"requests":requests,"inference_calls":calls,"status":"running",
  "scope":"Authored trusted-SDK engineering fixture; no hard isolation or C5/C6/scientific qualification"}
 def save(): (out/"edi-native-loop3-result.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
 save()
 try:
  for turn in range(4):
   current=investigation.step()
   ep=runtime.reasoning.get("native-neutral-loop3:inquiry:"+str(turn))
   response=ep.responses[-1]
   report["turns"].append({"turn":turn,"state":current["state"],
    "stop_reason":current.get("stop_reason"),"rationale":response.rationale_summary,
    "operation_proposals":[x.model_dump(mode="json") for x in response.operation_proposals],
    "input_tokens":response.input_tokens,"output_tokens":response.output_tokens,
    "hypothesis_count":len(response.hypotheses),"candidate_count":len(response.candidates)})
   report["current_state"]=current;save()
   if current["state"]!="ready":break
  before_calls,before_requests=len(calls),len(requests)
  reopened=Investigation(runtime,connector,gateway,wp.database,"native-neutral-loop3",
   max_turns=4,max_tokens=65536,session_seconds=600)
  original=investigation.state();replayed=reopened.state()
  assert replayed==original and len(calls)==before_calls and len(requests)==before_requests
  report.update(status="closed" if original["state"]=="completed" and closed else "incomplete",
   durable_controller_state_reopen=True,final_reports=closed,
   successful_information_reads=sum(x["operation"]=="read" and x["http_status"]==200 for x in requests))
 except Exception as error:
  report.update(status="failed",error_type=type(error).__name__,error=str(error)[:2000]);traceback.print_exc()
 finally:
  server.shutdown();server.server_close();thread.join()
  report["total_input_tokens"]=sum(x["input_tokens"] or 0 for x in calls)
  report["total_output_tokens"]=sum(x["output_tokens"] or 0 for x in calls)
  report["usage_unknown"]=any(x["input_tokens"] is None or x["output_tokens"] is None for x in calls)
  save()
 return report
