"""Common public tool binding. No state/evaluator reads or ecological policy.

IDs come only from this arm's already committed public responses. The native
broker remains the action authority; constrained decoding does not execute tools.
"""
import copy
import csv
import io
import json
from pathlib import Path
import sqlite3

VERSION = "public-tool-binding/1.0"
GUIDANCE = (
    "Complete the assigned investigation and submit a detailed final report through the public submit tool. "
    "Start with public discovery when document/stand IDs are unknown: search with an empty query browses the catalogue. "
    "Read relevant discovered documents; catalogue titles alone are not observations. Public IDs below are separate "
    "from EDI evidence record IDs, source IDs and hypothesis IDs. A failed request is not an observation. "
    "Do not repeat a rejected request unchanged. Change the request based on its diagnostic or discover missing inputs. "
    "Use the public argument shapes exactly, including kind=treat or harvest. No operator policy is supplied. "
    "Use available decisions for evidence, explicit competing explanations, prospective predictions/tests, decisions "
    "and observed outcomes. Fulfil the mission horizon and obligations before closing where feasible. "
    "Reserve the last decisions for status and a truthful submit: evidence, hypotheses/rivals, what happened, "
    "recommendations, forecasts and limitations. A yield without a report is an incomplete investigation.")

def obj(properties=None, required=()):
    return {"type":"object", "properties":properties or {}, "required":list(required), "additionalProperties":False}

def text(): return {"type":"string"}
def integer(lo, hi): return {"type":"integer", "minimum":lo, "maximum":hi}
def number(lo, hi): return {"type":"number", "minimum":lo, "maximum":hi}

class PublicProtocol:
    def __init__(self, directory, manual):
        self.path = Path(directory)/"cedar-world/run.sqlite"
        self.manual = manual
        self.failures = []
        self.decisions = 0
        self._before = 0
        self._intent = None

    def _rows(self):
        # SQL allowlist intentionally excludes state, identity and evaluator.
        with sqlite3.connect(self.path.resolve().as_uri()+"?mode=ro", uri=True) as db:
            events = [(op,json.loads(raw)) for op,raw in db.execute("SELECT operation,response FROM events ORDER BY rowid")]
            attempts = [(op,status) for op,status in db.execute("SELECT operation,status FROM attempts ORDER BY rowid")]
        return events,attempts

    def begin(self, proposal):
        self._before = len(self._rows()[1])
        self.decisions+=1
        self._intent = None
        if isinstance(proposal.get("operation"),dict):
            p=proposal["operation"]; self._intent={"operation":p["name"],"body":p["args"]}
        else:
            for p in proposal.get("operation_proposals",[]):
                if p["operation"]=="world-call": self._intent=p["arguments"]
                elif p["operation"]=="acquire-asset":
                    self._intent={"operation":"read","body":p["arguments"]}

    def finish(self):
        events,attempts=self._rows()
        new=attempts[self._before:]
        if any(status!=200 for _,status in new):
            self.failures.append({"intent":self._intent,"attempts":new,"at_public_event_count":len(events)})
        self._intent=None

    def snapshot(self):
        events,attempts=self._rows()
        failures=list(self.failures)
        pending=attempts[self._before:]
        if self._intent is not None and any(status!=200 for _,status in pending):
            failures.append({"intent":self._intent,"attempts":pending,"at_public_event_count":len(events)})
        documents={};people={};sources={};stands=set(); acquired=set();year=0
        def visit(value):
            if isinstance(value,dict):
                for k,v in value.items():
                    if k.lower() in ("stand_id","plot_id","stand","plot") and isinstance(v,str) and v:
                        stands.add(v)
                    visit(v)
            elif isinstance(value,list):
                for v in value:visit(v)
        for op,response in events:
            if op=="sources":
                for x in response.get("sources",[]):sources[x["id"]]=x.get("name",x.get("description",""))[:120]
            if op=="people":
                for x in response.get("people",[]):people[x["id"]]=x.get("role","")[:120]
            if op=="search":
                for x in response.get("items",[]):documents[x["id"]]=x.get("title","")[:160]
            if op=="ask":
                for x in response.get("materials",[]):
                    if "document_id" in x:documents[x["document_id"]]=x.get("title","")[:160]
            if op=="read":
                if "id" in response:
                    documents[response["id"]]=response.get("title","")[:160];acquired.add(response["id"])
                body=response.get("body","")
                if isinstance(body,str):
                    try:visit(json.loads(body))
                    except (ValueError,TypeError):pass
                    try:
                        for row in csv.DictReader(io.StringIO(body)):visit(row)
                    except (csv.Error,TypeError):pass
            visit(response)
            if type(response.get("year")) is int:year=response["year"]
        for failure in failures:
            p=failure.get("intent") or {}
            if p.get("operation") in ("read","records") and any(s==404 for _,s in failure["attempts"]):
                documents.pop(p.get("body",{}).get("document_id"),None)
        if len(documents)>512 or len(stands)>128 or len(people)>128:
            raise ValueError("Public identifier registry exceeds reviewed limits")
        latest=events[-1] if events else None
        # Prevent unchanged retries at a fixed public cut. A newly successful
        # discovery/status result changes the cut and permits reconsideration.
        blocked=sorted({(f.get("intent") or {}).get("operation") for f in failures
                        if f["at_public_event_count"]==len(events)}-{None})
        return {"version":VERSION,"decision":self.decisions,"remaining_decisions":64-self.decisions,
                "public_year":year,"documents":documents,"acquired_document_ids":sorted(acquired),
                "people":people,"sources":sources,"stand_ids":sorted(stands),
                "public_event_count":len(events),"public_attempt_count":len(attempts),
                "blocked_operations_at_this_cut":blocked,"recent_failures":failures[-2:],
                "last_public_receipt":json.dumps(latest,ensure_ascii=False)[:9000] if latest else None}

def public_shapes(view):
    docs=list(view["documents"]);people=list(view["people"]);stands=view["stand_ids"]
    shapes={"mission":obj(),"sources":obj(),"people":obj(),"status":obj(),
      "search":obj({"query":text(),"source":text(),"offset":integer(0,100000),"limit":integer(1,100)}),
      "advance":obj({"years":integer(1,5)}),
      "propose":obj({"objective":text(),"reason":text()},["objective","reason"]),
      "submit":obj({"conclusion":{"type":"string","minLength":1,"maxLength":20000},
                    "recommendations":{"type":"array","items":text()},"uncertainties":{"type":"array","items":text()},
                    "evidence_ids":{"type":"array","items":{"type":"string","enum":view["acquired_document_ids"]}}}
                   if view["acquired_document_ids"] else
                   {"conclusion":{"type":"string","minLength":1,"maxLength":20000},"recommendations":{"type":"array","items":text()},"uncertainties":{"type":"array","items":text()}},["conclusion"])}
    if docs:
        shapes["read"]=obj({"document_id":{"enum":docs},"include_asset":{"type":"boolean"},
                            "asset_offset":integer(0,100000000),"asset_limit":integer(1,65536)},["document_id"])
        shapes["records"]=obj({"document_id":{"enum":docs},"offset":integer(0,1000000),"limit":integer(1,200)},["document_id"])
    if people:shapes["ask"]=obj({"person_id":{"enum":people},"question":text()},["person_id","question"])
    if stands:
        plots={"type":"array","items":{"enum":stands},"minItems":1,"maxItems":12}
        shapes["measure"]=obj({"plots":plots,"metric":{"enum":["insects","enemies","foliage","fir","spruce","birch","age"]}},["plots","metric"])
        shapes["act"]={"anyOf":[
          obj({"kind":{"const":"treat"},"plots":plots,"method":{"enum":["broad","selective"]},"dose":number(0,1),"year":integer(view["public_year"]+1,view["public_year"]+5)},["kind","plots","method","dose"]),
          obj({"kind":{"const":"harvest"},"plots":plots,"fraction":number(0,.35),"year":integer(view["public_year"]+1,view["public_year"]+5)},["kind","plots","fraction"])]}
    return {k:v for k,v in shapes.items() if k not in view["blocked_operations_at_this_cut"]}

def bind_schema(schema, arm, view):
    schema=copy.deepcopy(schema);shapes=public_shapes(view)
    if arm=="baseline":
        branches=[obj({"name":{"const":op},"args":shape},["name","args"]) for op,shape in shapes.items()]
        branches += [obj({"name":{"const":"notes_replace"},"args":obj({"text":text()},["text"])},["name","args"]),
                     obj({"name":{"const":"history_search"},"args":obj({"text":text(),"offset":integer(0,1000000),"limit":integer(1,20)},["text","offset","limit"])},["name","args"]),
                     obj({"name":{"const":"history_read"},"args":obj({"id":integer(1,1000000),"offset":integer(0,4000000),"limit":integer(1,65536)},["id","offset","limit"])},["name","args"]),
                     obj({"name":{"const":"yield"},"args":obj({"reason":text()},["reason"])},["name","args"])]
        schema["properties"]["operation"]={"anyOf":branches}
    else:
        proposals=schema["$defs"]["OperationProposal"]["anyOf"]
        kept=[]
        for branch in proposals:
            op=branch["properties"]["operation"]["const"]
            if op=="world-call":
                branch["properties"]["arguments"]={"anyOf":[obj({"schema_version":{"const":"1.0"},"operation":{"const":name},"body":shape},["operation","body"]) for name,shape in shapes.items()]}
            if op=="acquire-asset":
                if not view["documents"] or "read" not in shapes:continue
                branch["properties"]["arguments"]=obj({"document_id":{"enum":list(view["documents"])}},["document_id"])
            if op=="teacher-review":continue
            kept.append(branch)
        schema["$defs"]["OperationProposal"]["anyOf"]=kept
        schema["properties"]["operation_proposals"]["maxItems"]=1
    return schema
