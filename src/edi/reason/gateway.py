"""C4 explicit inference dispatch. No provider call occurs at import or construction."""
import base64
from hashlib import sha256
from io import BytesIO
import json
from threading import Lock
from urllib.parse import urlsplit

from edi.observe.benchmark import http_json
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.contracts import Response
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class NativeGateway:
    """Provider-neutral job binding, C1 model-output capture and uncertain cost journal.

    count_tokens must apply the pinned backend chat template/processor to the exact
    messages. An estimate or missing tokenizer cannot authorize a model request.
    send returns (wire_json_bytes, response_json_text, input_tokens, output_tokens).
    Tests may inject authored transports, but must label them as authored fixtures.
    """
    def __init__(self, runtime, binding, journal_path, send, count_tokens, *, attribution,
                 max_calls=64, max_images=2, max_image_bytes=65536):
        if binding.model_id == "unbound" or binding.revision == "unbound" or binding.tokenizer_revision == "unknown":
            raise EDIError(ErrorCode.UNAVAILABLE, "native inference requires pinned model and tokenizer")
        self.runtime, self.binding, self.send, self.count_tokens = runtime, binding, send, count_tokens
        self.attribution, self.max_images, self.max_image_bytes = attribution, max_images, max_image_bytes
        if runtime.reasoning.profile.database.resolve() != journal_path.resolve():
            raise EDIError(ErrorCode.INVALID, "inference journal must use initialized C4 owner database")
        self.journal = CallJournal(journal_path, "inference_c4", max_calls=max_calls, max_bytes=128 * 1024**2)
        self.lock = Lock()
        self.origin = runtime.register_origin(OriginSpec(namespace="edi.model.outputs", native_source_id=binding.model_id,
            epoch=binding.revision, deliverer=binding.provider, channel="inference-response", adapter="edi-native-gateway/1.0", binding_basis="configured",
            descriptor={"binding": binding.model_dump(mode="json"), "attribution": attribution}))

    def messages(self, job, episode):
        if job.binding != self.binding or job.context_sha256 != episode.context.sha256:
            raise EDIError(ErrorCode.INTEGRITY, "gateway binding/context differs from pending native job")
        exported = self.runtime.reasoning.export_job(episode.request.inquiry_id, job.job_id)
        earlier = {j.job_id for j in episode.jobs[:next(i for i, j in enumerate(episode.jobs) if j.job_id == job.job_id)]}
        exported["data"] = {"inquiry": episode.request.model_dump(mode="json"), "context": episode.context.model_dump(mode="json"),
            "prior_responses": [r.model_dump(mode="json") for r in episode.responses if r.job_id in earlier]}
        control = {**exported["control"], "response_identity": {"workspace_id": episode.request.workspace_id,
            "inquiry_id": episode.request.inquiry_id, "job_id": job.job_id, "context_sha256": episode.context.sha256,
            "binding": job.binding.model_dump(mode="json"), "origin": "external-model-output"},
            "operation_rules": "At most one operation_proposals entry. Propose an ordinary public operation, explicit acquired-asset read, context selection, supported analysis, teacher review or yield. Proposals are not executed calls. Never request operator admission or adoption."}
        control["response_identity"].update(request_id="gateway:" + job.job_id, response_id="gateway:" + job.job_id)
        parts = [{"type": "text", "text": canonical(exported["data"])}]
        image_refs = []
        for item in episode.context.evidence:
            if item.media_type.split(";")[0] not in ("image/png", "image/jpeg"):
                continue
            if item.reference.selector != "whole-object" or item.selected_bytes > self.max_image_bytes or item.critical_profiles:
                raise EDIError(ErrorCode.UNSUPPORTED, "image inference requires a whole bounded selected native image")
            if len(image_refs) >= self.max_images:
                raise EDIError(ErrorCode.CAPACITY, "selected image count exceeds gateway profile")
            data = self.runtime.reader_for("C4").read_payload(item.reference.record_id, length=item.selected_bytes)
            if sha256(data).hexdigest() != item.reference.sha256:
                raise EDIError(ErrorCode.INTEGRITY, "selected image no longer matches native context")
            parts.append({"type": "image_url", "image_url": {"url": "data:" + item.media_type.split(";")[0] + ";base64," + base64.b64encode(data).decode()}})
            image_refs.append(item.reference.model_dump(mode="json"))
        return [{"role": "system", "content": canonical(control)}, {"role": "user", "content": parts}], image_refs

    def complete(self, job, episode):
        if not self.lock.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "native inference worker already in use")
        try:
            messages, images = self.messages(job, episode)
            if self.count_tokens is None:
                raise EDIError(ErrorCode.UNAVAILABLE, "exact pinned tokenizer/processor is not configured")
            count = self.count_tokens(messages)
            if type(count) is not int or count < 0 or count > job.input_token_cap:
                raise EDIError(ErrorCode.CAPACITY, "complete rendered multimodal input exceeds job cap")
            body = {"job": job.model_dump(mode="json", exclude={"status", "response_id"}), "messages_sha256": digest(messages), "images": images,
                    "input_tokens_preflight": count, "binding": self.binding.model_dump(mode="json")}
            prior = self.journal.begin(job.job_id, body)
            if prior["state"] == "completed":
                return Response.model_validate_json(canonical(json.loads(prior["result"])["response"]))
            if not self.journal.claim_once(job.job_id):
                raise EDIError(ErrorCode.UNKNOWN_COMMIT, "model dispatch completion/cost unresolved; no automatic inference retry")
            wire, output, input_tokens, output_tokens = self.send(messages, job)
            receipt = self.runtime.observe(Capture(origin_ref=self.origin.origin_ref,
                idempotency_key="model:" + job.job_id, kind="model-response", media_type="application/json", origin_class="generated",
                lineage=("native-inference-gateway/1.0", self.binding.model_id, self.binding.revision, job.job_id),
                profiles={"context_sha256": episode.context.sha256, "messages_sha256": digest(messages), "input_tokens": input_tokens, "output_tokens": output_tokens},
                completeness="complete", expected_bytes=len(wire), expected_sha256=sha256(wire).hexdigest()), BytesIO(wire))
            raw = json.loads(output)
            # These are transport identities, not invented student content.
            identities = {"workspace_id": episode.request.workspace_id, "inquiry_id": episode.request.inquiry_id,
                "job_id": job.job_id, "context_sha256": job.context_sha256, "binding": job.binding.model_dump(mode="json"),
                "origin": "external-model-output", "request_id": "gateway:" + job.job_id, "response_id": "gateway:" + job.job_id}
            for key, value in identities.items():
                if key in raw and raw[key] != value:
                    raise EDIError(ErrorCode.INTEGRITY, "model returned conflicting native job identity")
                raw[key] = value
            raw.update(input_tokens=input_tokens, output_tokens=output_tokens, attribution=self.attribution)
            response = Response.model_validate_json(canonical(raw))
            # Validate usage before accepting; never make missing usage zero.
            if input_tokens is None or output_tokens is None:
                raise EDIError(ErrorCode.UNKNOWN_COMMIT, "model response recorded but usage unavailable; reconcile original call")
            if input_tokens > job.input_token_cap or output_tokens > job.output_token_cap:
                raise EDIError(ErrorCode.CAPACITY, "actual model usage exceeded reserved cap")
            self.journal.finish(job.job_id, {"response": response.model_dump(mode="json"), "raw_record_id": receipt.observation.record_id})
            return response
        finally:
            self.lock.release()


class VllmBackend:
    """Local serving transport; caller supplies exact pinned processor/token counter."""
    def __init__(self, endpoint, model_id, *, transport=http_json):
        p = urlsplit(endpoint)
        if p.scheme != "http" or p.hostname != "127.0.0.1" or p.path not in ("", "/") or not p.port or p.query or p.fragment or p.username:
            raise ValueError("vLLM must be a configured loopback service")
        self.endpoint, self.model_id, self.transport = endpoint.rstrip("/"), model_id, transport

    def __call__(self, messages, job):
        status, wire = self.transport(self.endpoint + "/v1/chat/completions", {"model": self.model_id, "messages": messages,
            "max_tokens": job.output_token_cap, "temperature": 0, "seed": 17}, {}, timeout=120)
        if status != 200:
            raise EDIError(ErrorCode.UNAVAILABLE, "vLLM inference returned non-success; original dispatch remains unresolved")
        raw = json.loads(wire)
        return wire, raw["choices"][0]["message"]["content"], raw.get("usage", {}).get("prompt_tokens"), raw.get("usage", {}).get("completion_tokens")


class OpenAITeacherBackend:
    """Selective GPT-6.1 Sol critic; exact same C4 cut, no tools or world access."""
    def __init__(self, api_key, *, transport=http_json):
        if not api_key:
            raise EDIError(ErrorCode.UNAVAILABLE, "teacher API credential is not configured")
        self.api_key, self.transport = api_key, transport

    def __call__(self, messages, job):
        if job.role != "teacher" or job.binding.model_id != "gpt-6.1-sol":
            raise EDIError(ErrorCode.DENIED, "teacher transport accepts GPT-6.1 Sol critique jobs only")
        inputs = []
        for message in messages:
            parts = [{"type": "input_text", "text": message["content"]}] if isinstance(message["content"], str) else [
                {"type": "input_text", "text": p["text"]} if p["type"] == "text" else {"type": "input_image", "image_url": p["image_url"]["url"]} for p in message["content"]]
            inputs.append({"role": message["role"], "content": parts})
        status, wire = self.transport("https://api.openai.com/v1/responses", {"model": "gpt-6.1-sol", "input": inputs,
            "max_output_tokens": job.output_token_cap, "reasoning": {"effort": "medium"}, "store": False},
            {"Authorization": "Bearer " + self.api_key}, timeout=120)
        if status != 200:
            raise EDIError(ErrorCode.UNAVAILABLE, "teacher returned non-success; original dispatch remains unresolved")
        raw = json.loads(wire)
        if raw.get("status") != "completed":
            raise EDIError(ErrorCode.INCOMPLETE, "teacher response is incomplete; do not treat partial output as a critique")
        output = "".join(p["text"] for item in raw.get("output", []) for p in item.get("content", []) if p.get("type") == "output_text")
        usage = raw.get("usage", {})
        return wire, output, usage.get("input_tokens"), usage.get("output_tokens")
