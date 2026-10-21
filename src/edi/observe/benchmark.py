"""C1 exact-byte acquisition; C0 journal plus C7 authority gate world requests."""
import base64
from hashlib import sha256
from io import BytesIO
import json
from threading import RLock
import urllib.error
import urllib.request

from edi.agency.benchmark import PublicIntent
from edi.observe.contracts import Capture, OriginSpec
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise EDIError(ErrorCode.DENIED, "external redirects are forbidden")


def http_json(url, payload, headers, *, timeout=60, max_bytes=1024 * 1024):
    req = urllib.request.Request(url, data=canonical(payload).encode(), headers={"Content-Type": "application/json", **headers}, method="POST")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        response = opener.open(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise EDIError(ErrorCode.CAPACITY, "response exceeds admitted transport budget")
        return response.code, data


class BrokerConnector:
    def __init__(self, runtime, endpoint, token, session_id, authority, journal_path, *, max_requests=300, transport=http_json):
        if len(token) < 24:
            raise ValueError("a fresh broker token of at least 24 characters is required")
        # Endpoint validation is owned by adopted authority, including token binding.
        if authority.grant.endpoint.rstrip("/") != endpoint.rstrip("/") or authority.grant.token_sha256 != sha256(token.encode()).hexdigest():
            raise EDIError(ErrorCode.DENIED, "connector and adopted broker authority differ")
        self.runtime, self.endpoint, self.token = runtime, endpoint.rstrip("/"), token
        self.session_id, self.authority, self.transport = session_id, authority, transport
        if runtime.workflow.profile.database.resolve() != journal_path.resolve():
            raise EDIError(ErrorCode.INVALID, "broker intent journal must use initialized C0 owner database")
        self.journal = CallJournal(journal_path, "benchmark_c0", max_calls=max_requests, max_bytes=512 * 1024**2)
        self.lock = RLock()
        self.origin = runtime.register_origin(OriginSpec(namespace="benchmark.public", native_source_id=session_id, epoch="1",
            deliverer="broker-loopback", channel="public-api", adapter="edi-broker/1.0", binding_basis="configured",
            descriptor={"limits": "constructed world, public observations only"}))

    def _capture(self, request_id, raw, *, suffix="response", media="application/json", profiles=None, origin_class="simulation"):
        return self.runtime.observe(Capture(origin_ref=self.origin.origin_ref, idempotency_key="benchmark:" + digest([request_id, suffix]),
            kind="constructed-world-public", media_type=media, origin_class=origin_class, lineage=("broker-acquisition-v1", self.session_id, request_id, suffix),
            profiles=profiles or {}, completeness="complete", expected_bytes=len(raw), expected_sha256=sha256(raw).hexdigest()), BytesIO(raw))

    def call(self, intent: PublicIntent):
        intent = PublicIntent.model_validate_json(intent.model_dump_json())
        if len(canonical(intent.body).encode()) > 131072:
            raise EDIError(ErrorCode.CAPACITY, "broker request exceeds public body limit")
        self.authority.authorize(intent)
        rid = intent.body["request_id"]
        with self.lock:
            old = self.journal.begin(rid, {"session": self.session_id, "operation": intent.operation, "body": intent.body})
            if old["state"] == "completed":
                return json.loads(old["result"])
            # Broker deduplicates exact requests even after a lost transport receipt.
            self.journal.attempt(rid)
            status, raw = self.transport(self.endpoint + "/v2/" + intent.operation, intent.body, {"Authorization": "Bearer " + self.token})
            parsed = json.loads(raw, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
            receipt = self._capture(rid, raw, profiles={"operation": intent.operation, "http_status": status})
            result = {"http_status": status, "body": parsed, "evidence_record_id": receipt.observation.record_id,
                      "sha256": sha256(raw).hexdigest(), "response_bytes": len(raw)}
            self.journal.finish(rid, result)
            return result

    def acquire_asset(self, document_id, acquisition_id, *, max_bytes=16 * 1024**2):
        """Bounded reassembly is explicit selected work, not hidden source retrieval."""
        blocks, offset, expected, total, fmt = [], 0, None, None, None
        while True:
            result = self.call(PublicIntent(operation="read", body={"request_id": acquisition_id + ":" + str(offset), "document_id": document_id,
                "include_asset": True, "asset_offset": offset, "asset_limit": 65536}))
            if result["http_status"] != 200:
                raise EDIError(ErrorCode.UNAVAILABLE, "asset read failed; original response retained")
            body, asset = result["body"], result["body"].get("asset")
            if not asset or asset.get("encoding") != "base64" or asset.get("offset") != offset:
                raise EDIError(ErrorCode.INTEGRITY, "asset range response differs from selected request")
            if expected is None:
                expected, total, fmt = body.get("sha256"), asset["total_bytes"], body.get("format")
            if body.get("sha256") != expected or asset["total_bytes"] != total or total > max_bytes:
                raise EDIError(ErrorCode.CAPACITY if total > max_bytes else ErrorCode.INTEGRITY, "asset identity changed or byte budget exceeded")
            part = base64.b64decode(asset["data"], validate=True)
            if len(part) > 65536 or offset + len(part) > total or (not part and asset["has_more"]):
                raise EDIError(ErrorCode.INTEGRITY, "invalid asset chunk length")
            blocks.append(part); offset += len(part)
            if not asset["has_more"]:
                break
        data = b"".join(blocks)
        if offset != total or sha256(data).hexdigest() != expected:
            raise EDIError(ErrorCode.INTEGRITY, "reassembled native asset digest mismatch")
        media = {"png":"image/png", "jpeg":"image/jpeg", "json":"application/json", "csv":"text/csv", "txt":"text/plain", "wav":"audio/wav", "pdf":"application/pdf"}.get(fmt, "application/octet-stream")
        receipt = self._capture(acquisition_id, data, suffix="native-asset", media=media,
            origin_class="external" if body.get("source") == "external" else "simulation",
            profiles={"document_id": document_id, "native_sha256": expected, "format": fmt, "original_origin": body.get("origin"),
                "source_metadata": body.get("metadata", {}), "derived_is_independent_evidence": False})
        return receipt.observation
