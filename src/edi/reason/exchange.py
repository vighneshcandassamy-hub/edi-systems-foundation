"""Explicit file handoff for a teacher without a paid inference API.

No browser, subscription API, credential or model is invoked. The operator
supplies feedback from the declared teacher, against the exported original cut.
"""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

from pydantic import ValidationError

from edi.observe.contracts import Capture, OriginSpec
from edi.reason.contracts import Response
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class AwaitingModelResponse(EDIError):
    def __init__(self, job_id, request_path):
        super().__init__(ErrorCode.INCOMPLETE, "Teacher feedback is awaiting explicit file import")
        self.job_id, self.request_path = job_id, str(request_path)


class AwaitingModelAvailability(EDIError):
    def __init__(self, job_id, diagnostic):
        super().__init__(ErrorCode.UNAVAILABLE, diagnostic)
        self.job_id = job_id


class ModelOutputRejected(EDIError):
    def __init__(self, receipt):
        super().__init__(ErrorCode.INVALID, receipt["diagnostic"])
        self.receipt = receipt


def stored_result(row):
    value = json.loads(row["result"])
    if value.get("outcome") == "rejected":
        raise ModelOutputRejected(value)
    return Response.model_validate_json(canonical(value["response"]))


class TeacherExchangeGateway:
    """C4-owned request/result journal and C1 generated-output provenance.

    Provider identity and token counts are operator-declared, not authenticated
    or independently measured. Missing usage consumes the full job reservation
    in C0. Exported requests may include selected images as data URLs.
    """
    def __init__(self, runtime, binding, journal_path, directory, *, attribution, max_calls=64):
        if binding != runtime.reasoning.profile.teacher or binding.model_id == "unbound" or binding.revision == "unbound":
            raise EDIError(ErrorCode.INVALID, "exchange must match the pinned C4 teacher binding")
        if journal_path.resolve() != runtime.reasoning.profile.database.resolve():
            raise EDIError(ErrorCode.INVALID, "teacher exchange journal belongs to C4")
        self.runtime, self.binding, self.attribution = runtime, binding, attribution
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.journal = CallJournal(journal_path, "teacher_exchange_c4", max_calls=max_calls, max_bytes=128 * 1024**2)
        self.origin = runtime.register_origin(OriginSpec(namespace="edi.teacher.feedback", native_source_id=binding.model_id,
            epoch=binding.revision, deliverer="explicit-operator-import", channel="teacher-feedback",
            adapter="edi-teacher-exchange/1.0", binding_basis="configured",
            descriptor={"binding": binding.model_dump(mode="json"), "identity": "operator-declared; unauthenticated"}))

    def request_path(self, job_id):
        return self.directory / (sha256(job_id.encode()).hexdigest() + ".request.json")

    def complete(self, job, episode):
        if job.role != "teacher" or job.binding != self.binding or job.context_sha256 != episode.context.sha256:
            raise EDIError(ErrorCode.INTEGRITY, "teacher exchange job/role/cut differs")
        from edi.reason.gateway import render_job_messages
        messages, images = render_job_messages(self.runtime, self.binding, job, episode)
        control = json.loads(messages[0]["content"])
        control["response_identity"].update(request_id="exchange:" + job.job_id, response_id="exchange:" + job.job_id)
        messages[0]["content"] = canonical(control)
        request = {"inquiry_id": episode.request.inquiry_id, "job": job.model_dump(mode="json", exclude={"status", "response_id"}), "messages": messages,
            "image_refs": images, "messages_sha256": digest(messages), "transport": "explicit-file-exchange",
            "feedback_content_fields": ["rationale_summary", "limitation", "feedback_disposition"] + (["procedural_guidance"] if job.teaching_stage == "critique" else []),
            "instructions": "Follow the recorded teaching stage against this exact cut. Independent assessment sees no current student draft; critique reviews both initial assessments. No world access, new evidence, tool execution or admission. Import through edi integration-teacher-import.",
            "cost_status": "usage unknown unless supplied; C0 charges the full reservation when unknown"}
        row = self.journal.begin(job.job_id, request, reserve_bytes=1024 * 1024)
        if row["state"] == "completed":
            return stored_result(row)
        path, payload = self.request_path(job.job_id), (canonical(request) + "\n").encode()
        # Exclusive create never replaces another cut under the same request file.
        try:
            with path.open("xb") as stream:
                stream.write(payload)
        except FileExistsError:
            if path.read_bytes() != payload:
                raise EDIError(ErrorCode.INTEGRITY, "teacher exchange file differs from original request")
        raise AwaitingModelResponse(job.job_id, path)

    def import_feedback(self, job_id, path):
        row = self.journal.get(job_id)
        if row is None:
            raise EDIError(ErrorCode.NOT_FOUND, "export the original teacher job before importing feedback")
        if row["state"] == "completed":
            raise EDIError(ErrorCode.CONFLICT, "teacher feedback already retained; original result is immutable")
        request = json.loads(row["request"])
        job = request["job"]
        with Path(path).open("rb") as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise EDIError(ErrorCode.CAPACITY, "teacher feedback file exceeds one MiB")
        # Raw bytes retained even when content admission fails. A submission ID
        # identifies bytes, not a second provider inference or independent source.
        try:
            content = json.loads(raw)
        except (ValueError, UnicodeError):
            content = None
        supplied = content.get("usage", {}) if isinstance(content, dict) else {}
        usage = supplied if isinstance(supplied, dict) else {}
        usage_error = not isinstance(supplied, dict)
        input_tokens, output_tokens = usage.get("input_tokens"), usage.get("output_tokens")
        if any(x is not None and (type(x) is not int or x < 0) for x in (input_tokens, output_tokens)):
            usage_error = True
            input_tokens = output_tokens = None
        receipt = self.runtime.observe(Capture(origin_ref=self.origin.origin_ref,
            idempotency_key="teacher:" + job_id + ":" + sha256(raw).hexdigest(), kind="teacher-feedback",
            media_type="application/json", origin_class="generated",
            lineage=("explicit-teacher-exchange/1.0", self.binding.model_id, self.binding.revision, job_id),
            profiles={"context_sha256": job["context_sha256"], "input_tokens": input_tokens,
                "output_tokens": output_tokens, "usage_basis": "operator-declared; not independently measured"},
            expected_bytes=len(raw), expected_sha256=sha256(raw).hexdigest()), BytesIO(raw))
        result = {"raw_record_id": receipt.observation.record_id, "input_tokens": input_tokens, "output_tokens": output_tokens}
        try:
            if usage_error:
                raise ValueError("teacher usage requires an object with nonnegative integer or null counts")
            if not isinstance(content, dict) or set(content) - ({"rationale_summary", "limitation", "feedback_disposition", "usage"} | ({"procedural_guidance"} if job.get("teaching_stage") == "critique" else set())):
                raise ValueError("feedback permits rationale_summary, limitation, feedback_disposition, optional usage and critique-stage procedural_guidance")
            if usage and set(usage) - {"input_tokens", "output_tokens"}:
                raise ValueError("usage permits only input_tokens and output_tokens")
            response = Response.model_validate_json(canonical({
                **{key: value for key, value in content.items() if key != "usage"},
                "workspace_id": self.runtime.profile.workspace_id,
                "inquiry_id": request["inquiry_id"],
                "request_id": "exchange:" + job_id, "response_id": "exchange:" + job_id,
                "job_id": job_id, "context_sha256": job["context_sha256"],
                "binding": self.binding.model_dump(mode="json"), "origin": "external-model-output",
                "attribution": self.attribution, "input_tokens": input_tokens, "output_tokens": output_tokens}))
            if response.feedback_disposition == "not-applicable":
                raise ValueError("teacher feedback needs retained-for-review, challenged or deferred disposition")
            if ((input_tokens is not None and input_tokens > job["input_token_cap"]) or
                    (output_tokens is not None and output_tokens > job["output_token_cap"])):
                raise ValueError("declared usage exceeds the original teacher reservation")
        except (ValidationError, ValueError, TypeError, KeyError) as exc:
            result.update(outcome="rejected", diagnostic=str(exc)[:8192])
            self.journal.finish(job_id, result)
            raise ModelOutputRejected(result) from exc
        result.update(outcome="returned", response=response.model_dump(mode="json"))
        self.journal.finish(job_id, result)
        return {"job_id": job_id, "raw_record_id": result["raw_record_id"], "status": "retained; C0/C4 admission pending"}

    def receipt(self, job_id):
        row = self.journal.get(job_id)
        return json.loads(row["result"]) if row and row["state"] == "completed" else None
