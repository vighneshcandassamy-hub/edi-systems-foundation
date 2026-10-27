"""Fresh paired Cedar brokers and public-only baseline/native EDI adapters.

No model provider is implemented. Call construction explicitly on Kaggle only.
Operator-only fingerprints and evaluation never enter participant packets.
"""
from datetime import timedelta
from hashlib import sha256
import json
import os
from pathlib import Path
import secrets
import sqlite3
import uuid
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler
from urllib.error import HTTPError
from offline_runner import Baseline, BoundaryError, Limits, NativeEDI, Pair, fingerprint, wire


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise BoundaryError("Public world redirect forbidden")


class CedarPublic:
    def __init__(self, world_module, directory, limits):
        self.world, self.out, self.limits = world_module, Path(directory).resolve(), limits
        self.out.mkdir(parents=True, exist_ok=False)
        self.token = secrets.token_urlsafe(32)
        self.server = world_module.start_world(self.out, self.token, port=0)
        self.endpoint = "http://127.0.0.1:" + str(self.server.server_port)
        self.closed = False

    def call(self, operation, body):
        if self.closed or operation not in self.world.PUBLIC_OPERATIONS:
            raise BoundaryError("Closed or unauthorized public world operation")
        raw = wire(body).encode()
        if len(raw) > 131072:
            raise BoundaryError("Native public body cap exceeded")
        req = Request(self.endpoint + "/v2/" + operation, data=raw, method="POST",
                      headers={"Content-Type":"application/json", "Authorization":"Bearer " + self.token})
        opener = build_opener(ProxyHandler({}), NoRedirect())
        try: response = opener.open(req, timeout=60)
        except HTTPError as exc: response = exc
        with response:
            answer = response.read(1024**2 + 1)
            if len(answer) > 1024**2:
                raise BoundaryError("Native public return cap exceeded; reconcile outcome before retry")
            status = response.code
        data = json.loads(answer)
        terminal = operation == "submit" and status == 200 and data.get("status") == "accepted"
        self.closed = terminal
        return {"http_status":status, "body":data, "closed":terminal}

    def snapshot(self):
        # Trusted operator audit only; never use as model evidence.
        with sqlite3.connect((self.out/"cedar-world/run.sqlite").as_uri()+"?mode=ro", uri=True) as db:
            state = json.loads(db.execute("SELECT payload FROM state WHERE id=1").fetchone()[0])
            events = [(r[0],r[1]) for r in db.execute("SELECT id,operation FROM events ORDER BY rowid")]
        return {"state_sha256":fingerprint(state), "events":events}

    def stop(self):
        if self.server is not None:
            self.server.shutdown(); self.server.server_close(); self.server = None


def application_profile(out, model, world, limits):
    from edi.inquiry.application import ApplicationProfile
    from edi.reason.contracts import ModelBinding
    from edi.shared.contracts import utc_now
    from edi.shared.durable_io import canonical, digest
    now = utc_now(); identity = "cedar-comparison-" + uuid.uuid4().hex[:16]
    binding = ModelBinding(model_id=model["id"], revision=model["revision"],
        provider="comparison-explicit-file-exchange", engine="no-provider-connected",
        tokenizer_revision="unmeasured-policy-reservation")
    profile = ApplicationProfile.model_validate_json(canonical({
        "application_id":identity, "run_id":identity,
        "observation":{"workspace_id":identity,"database":str(out/"owners.sqlite3")},
        "student":{"mode":"file-exchange","binding":binding,
            "directory":str(out/"reasoner-exchange"),"max_images":1,
            "max_request_bytes":limits.max_request_bytes,"max_model_len":16384,
            "attribution":"Comparison exchange; model provider identity/isolation/usage require independent qualification"},
        "teacher":{"mode":"disabled","binding":ModelBinding()},
        "agency":{"workspace_id":identity,"database":str(out/"owners.agency.sqlite3"),"operator_ids":["engineering-operator"]},
        "broker":{"grant":{"grant_id":identity,"session_id":identity,"workspace_id":identity,
            "endpoint":world.endpoint,"token_sha256":sha256(world.token.encode()).hexdigest(),
            "mission_sha256":digest(world.world.MISSION),"public_operations":world.world.PUBLIC_OPERATIONS,
            "operator_id":"engineering-operator","not_before":(now-timedelta(seconds=1)).isoformat(),
            "expires_at":(now+timedelta(seconds=limits.max_seconds)).isoformat(),
            "operations":list(world.world.PUBLIC_OPERATIONS),"maximum_requests":limits.max_public_calls}},
        "teaching_mode":"selective","use_teaching_memory":False,
        "max_turns":limits.max_decisions,"max_tokens":limits.max_reserved_tokens,
        "session_seconds":limits.max_seconds,"max_corrections":1}))
    (out/"application.json").write_text(profile.model_dump_json(indent=2))
    return profile


class CedarPair:
    def __init__(self, source, directory, model, limits=Limits()):
        if limits.input_token_cap != 12288 or limits.output_token_cap != 4096:
            raise BoundaryError("Native Cedar composition fixes 12288/4096 job caps")
        self.source, self.directory = Path(source).resolve(), Path(directory).resolve()
        if self.directory.exists():
            raise BoundaryError("New paired world directory required; original runs cannot be resumed")
        self.worlds = {}; self.native = None; self.pair = None
        from cedar_session import verify_source, CedarSession
        from edi.inquiry.application import IntegratedApplication
        import meadows_world
        self.manifest = verify_source(self.source)
        self.pair = Pair(self.directory, model, limits)
        try:
            for arm in ("baseline","edi"):
                self.worlds[arm] = CedarPublic(meadows_world, self.directory/arm/"native", limits)
            snapshots = {a:w.snapshot() for a,w in self.worlds.items()}
            if snapshots["baseline"]["state_sha256"] != snapshots["edi"]["state_sha256"]:
                raise BoundaryError("Initial private world states differ; no participant request exported")
            self.initial_state_sha256 = snapshots["baseline"]["state_sha256"]
            self.baseline = Baseline(self.pair.channels["baseline"], meadows_world.MISSION,
                                     meadows_world.PUBLIC_OPERATIONS, self.worlds["baseline"].call)
            rid = "bootstrap-baseline-" + uuid.uuid4().hex
            first = self.worlds["baseline"].call("mission", {"request_id":rid})
            if first["http_status"] != 200:
                raise BoundaryError("Public baseline mission bootstrap failed")
            # Count bootstrap in both the raw history and the public-call budget,
            # just as native C0/C7 count EDI's automatic mission acquisition.
            with self.baseline.db:
                self.baseline.db.execute("INSERT INTO actions VALUES (?,?,?,'completed',?)", (rid,"mission",wire({}),wire(first)))
                self.baseline.record("public-bootstrap",first)
                state = self.baseline.state(); state["latest"] = first; self.baseline.save(state)
            edi_world = self.worlds["edi"]
            profile = application_profile(edi_world.out, model, edi_world, limits)
            os.environ["EDI_BROKER_TOKEN"] = edi_world.token
            self.native = CedarSession(self.source, edi_world.out, token=edi_world.token)
            self.native.app = IntegratedApplication(profile)
            self.native.step()
            self.edi = NativeEDI(self.pair.channels["edi"], self.native)
            if self.worlds["baseline"].snapshot()["state_sha256"] != self.worlds["edi"].snapshot()["state_sha256"]:
                raise BoundaryError("Mission bootstrap mutated paired world parity")
            self._save("pair-initial-audit.json", {"initial_state_sha256":self.initial_state_sha256,
                "source_manifest_sha256":sha256((self.source/"source-manifest.json").read_bytes()).hexdigest(),
                "scope":"Operator-only parity evidence, never participant input", "provider_usage_scope":"Not measured by Cedar public/native bridge; consult external adapter ledger"})
        except Exception:
            self.close(); raise

    def _save(self, name, value):
        (self.directory/name).write_text(json.dumps(value,indent=2,allow_nan=False))

    def export(self, arm):
        if arm not in ("baseline","edi"):
            raise BoundaryError("Unknown comparison arm")
        packet = getattr(self, arm).export()
        encoded = wire(packet)
        if any(w.token in encoded for w in self.worlds.values()):
            raise BoundaryError("Broker credential appeared in participant packet")
        return packet

    def consume(self, arm, request_id, response_bytes):
        if arm not in ("baseline","edi"):
            raise BoundaryError("Unknown comparison arm")
        result = getattr(self,arm).consume(request_id,response_bytes)
        if arm == "baseline":
            terminal = self.baseline.state()["terminal"]
            if terminal:
                self.pair.mark_terminal(arm, "completed" if terminal == "completed" else "yielded" if terminal.startswith("yielded") else "failed")
        else:
            if result["state"] in ("completed","yielded"):
                self.pair.mark_terminal(arm,result["state"])
        return result

    def evaluate(self):
        import meadows_world
        # Pair.evaluate checks both terminal declarations before entering lambda.
        return self.pair.evaluate(lambda:{arm:meadows_world.evaluate_closed(w.out) for arm,w in self.worlds.items()})

    def close(self):
        for world in self.worlds.values(): world.stop()
        if self.pair is not None:
            for channel in self.pair.channels.values(): channel.db.close()
            self.pair.db.close()
            self.pair = None
