"""Finite authored information environment, independent of EDI's decisions.

No hypotheses, investigation sequence or model answers are supplied. These
fixtures are engineering inputs, not empirical evidence or a scientific test.
"""
import base64
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread, RLock

MISSION = {
    "objective": "Investigate the recorded change in instrument readings. Determine what the available information supports about the change and a next-reading prediction. Obtain information as needed, then submit findings, uncertainty and any further information needed.",
    "scope": "Authored neutral instrument engineering environment; no forest case or empirical science.",
    "public_operations": {
        "mission": {"body": {}, "returns": "original objective and access catalogue"},
        "sources": {"body": {}, "returns": "available document and interview identifiers"},
        "read": {"body": {"document_id": "catalogue document ID"}, "returns": "raw document, source attribution and digest"},
        "ask": {"body": {"person_id": "catalogue interview ID", "question": "your information request"}, "returns": "available interview record; unsupported requests remain unknown"},
        "status": {"body": {}, "returns": "session status"},
        "submit": {"body": {"conclusion": "findings and limitations"}, "returns": "closure receipt"},
    },
    "access_protocol": "Public operations use world-call with arguments {operation: public name, body: operation-specific object}. C0 assigns request_id. This catalogue defines available access, not an investigation sequence. Native EDI component operations and selective teacher review are also available through the configured controller.",
}
DOCUMENTS = {
    "m17": {"format": "csv", "description": "Instrument register export", "content": "sample_label,reading_bytes\n0,8\n1,12\n2,16\n"},
    "r22": {"format": "txt", "description": "Capture desk notebook", "content": "Register export batch A. Rows were transcribed from one prepared fixture. Sample labels preserve entry order. Clock readings were not retained. No independent repeat is filed in this batch. Author: capture desk.\n"},
    "b04": {"format": "txt", "description": "Instrument service bulletin", "content": "The dashboard has four display columns. Its enclosure has sixteen fasteners. Replacement labels are sold in packs of twelve. This bulletin records enclosure inventory; it contains no measurement of the registered quantity.\n"},
}
INTERVIEW = "Capture operator record: the sample labels are ordinal entries. Elapsed intervals and the mechanism generating these entries were not measured. There is no withheld repeat experiment or measured next sample in this engineering fixture. These statements are operator attribution, not an independent measurement."


def start_world(out, token, port=8098):
    out = Path(out)
    path = out / "world-session.json"
    ledger = json.loads(path.read_bytes()) if path.exists() else {"requests": [], "completed": {}, "conclusions": []}
    lock = RLock()

    def persist():
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
        temporary.replace(path)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            if self.headers.get("Authorization") != "Bearer " + token or not 0 < length <= 131072:
                status, answer = 403, {"error": "authorization or request bound"}
            else:
                body = json.loads(self.rfile.read(length))
                operation = self.path.removeprefix("/v2/")
                request_id = body.get("request_id")
                fingerprint = hashlib.sha256(json.dumps([operation, body], sort_keys=True).encode()).hexdigest()
                with lock:
                    previous = ledger["completed"].get(request_id)
                    if previous:
                        status, answer = ((previous["status"], previous["answer"]) if previous["fingerprint"] == fingerprint else (409, {"error": "request identity conflict"}))
                    else:
                        if not isinstance(request_id, str) or ledger["conclusions"]:
                            status, answer = 409, {"error": "invalid identity or closed session"}
                        elif operation == "mission" and set(body) == {"request_id"}:
                            status, answer = 200, {"mission": MISSION}
                        elif operation == "sources" and set(body) == {"request_id"}:
                            status, answer = 200, {"documents": [{"document_id": name, "format": doc["format"], "description": doc["description"]} for name, doc in DOCUMENTS.items()], "people": [{"person_id": "capture-operator", "description": "Available capture desk interview record"}]}
                        elif operation == "read" and body.get("document_id") in DOCUMENTS and set(body) <= {"request_id", "document_id", "include_asset", "asset_offset", "asset_limit"}:
                            name = body["document_id"]
                            doc = DOCUMENTS[name]
                            raw = doc["content"].encode()
                            status, answer = 200, {"document_id": name, "format": doc["format"], "source": "simulation", "sha256": hashlib.sha256(raw).hexdigest(), "content": doc["content"]}
                            if body.get("include_asset"):
                                offset, limit = body.get("asset_offset", 0), body.get("asset_limit", 65536)
                                if type(offset) is not int or type(limit) is not int or not 0 <= offset <= len(raw) or not 1 <= limit <= 65536:
                                    status, answer = 422, {"error": "invalid range"}
                                else:
                                    part = raw[offset:offset + limit]
                                    answer["asset"] = {"encoding": "base64", "offset": offset, "total_bytes": len(raw), "data": base64.b64encode(part).decode(), "has_more": offset + len(part) < len(raw)}
                        elif operation == "ask" and set(body) == {"request_id", "person_id", "question"} and body.get("person_id") == "capture-operator" and isinstance(body.get("question"), str) and body["question"]:
                            status, answer = 200, {"person_id": "capture-operator", "requested_question": body["question"], "available_record": INTERVIEW, "basis": "pre-authored attributed interview; no new experiment or outside retrieval"}
                        elif operation == "status" and set(body) == {"request_id"}:
                            status, answer = 200, {"closed": False, "unique_requests": len(ledger["completed"])}
                        elif operation == "submit" and set(body) == {"request_id", "conclusion"} and isinstance(body["conclusion"], str) and 0 < len(body["conclusion"]) <= 24000:
                            ledger["conclusions"].append(body["conclusion"])
                            status, answer = 200, {"status": "closed", "conclusion_received": True}
                        else:
                            status, answer = 422, {"error": "unsupported operation or arguments", "public_operations": MISSION["public_operations"]}
                        ledger["completed"][request_id] = {"fingerprint": fingerprint, "status": status, "answer": answer}
                    ledger["requests"].append({"operation": operation, "body": body, "http_status": status, "response": answer, "duplicate": previous is not None})
                    persist()
            data = json.dumps(answer, sort_keys=True, separators=(",", ":")).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    persist()
    return server
