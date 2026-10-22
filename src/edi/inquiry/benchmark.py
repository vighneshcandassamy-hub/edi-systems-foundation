"""C0 resumable investigator connecting existing owners and model roles.

The name is retained for API compatibility. No domain investigation sequence is
encoded here. Model trials/benchmarks require a separate explicit invocation.
"""
from datetime import timedelta
from io import BytesIO
import json
from threading import Lock

from pydantic import ValidationError

from edi.agency.benchmark import PublicIntent
from edi.interpret.contracts import InputSpec, InterpretRequest
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.contracts import Budget, EvidenceSelection, InquiryRequest, OutboxAck, RejectedResponse, StepRequest, SubmissionRequest
from edi.reason.exchange import AwaitingModelAvailability, AwaitingModelResponse, ModelOutputRejected
from edi.shared.contracts import utc_now
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class Investigation:
    """C0 phases coordinate native receipts; never infer missing completion.

    Local owner commands retain original request identities. Provider calls use
    their own C4 journals and cannot be resent on an unknown completion. Teacher
    file exchange is an explicit waiting input, not a failed model inference.
    """
    def __init__(self, runtime, connector, student_gateway, path, run_id, *, teacher_gateway=None,
                 max_turns=32, max_tokens=262144, session_seconds=3600, max_corrections=1):
        if not 1 <= len(run_id) <= 96 or max_turns < 1 or max_tokens < 1 or session_seconds <= 0 or max_corrections not in (0, 1):
            raise EDIError(ErrorCode.INVALID, "invalid bounded investigation configuration")
        if path.resolve() != runtime.workflow.profile.database.resolve():
            raise EDIError(ErrorCode.INVALID, "investigation journals belong to C0")
        if student_gateway.binding != runtime.reasoning.profile.student:
            raise EDIError(ErrorCode.INTEGRITY, "student gateway differs from C4 binding")
        if teacher_gateway is not None and teacher_gateway.binding != runtime.reasoning.profile.teacher:
            raise EDIError(ErrorCode.INTEGRITY, "teacher gateway differs from C4 binding")
        self.runtime, self.connector = runtime, connector
        runtime.reasoning.bind_inference(student_gateway, teacher_gateway)
        self.student, self.teacher = runtime.reasoning.student, (runtime.reasoning.teacher if teacher_gateway is not None else None)
        self.run_id, self.max_turns, self.max_tokens = run_id, max_turns, max_tokens
        self.max_corrections, self.lock = max_corrections, Lock()
        self.journal = CallJournal(path, "investigation_c0", max_calls=max_turns + 2, max_bytes=256 * 1024**2)
        self.phases = CallJournal(path, "investigation_phases_c0", max_calls=max_turns * 32 + 4, max_bytes=256 * 1024**2)
        previous = self.journal.get("configuration")
        if previous and json.loads(previous["request"]).get("controller") != "edi-c0/integrated-1.0":
            raise EDIError(ErrorCode.UNSUPPORTED, "use a fresh integration workspace; historical C0 state is not migrated")
        deadline = (json.loads(previous["request"])["deadline"] if previous else
                    (utc_now() + timedelta(seconds=session_seconds)).isoformat())
        self.deadline = deadline
        self.journal.begin("configuration", {"run_id": run_id, "session_id": connector.session_id,
            "workspace": runtime.profile.workspace_id, "student": student_gateway.binding.model_dump(mode="json"),
            "teacher": teacher_gateway.binding.model_dump(mode="json") if teacher_gateway else None,
            "max_turns": max_turns, "max_tokens": max_tokens, "session_seconds": session_seconds,
            "max_corrections": max_corrections, "deadline": deadline, "controller": "edi-c0/integrated-1.0"})
        self.journal.finish("configuration", {"frozen": True})
        self.origin = runtime.register_origin(OriginSpec(namespace="edi.component.results", native_source_id=run_id,
            epoch="1", deliverer="C0-native-ports", channel="component-results", adapter="edi-c0/integrated-1.0",
            binding_basis="configured", descriptor={"independent_world_evidence": False}))

    def _phase(self, key, body, operation):
        row = self.phases.begin(key, body, reserve_bytes=4 * 1024**2)
        if row["state"] == "completed":
            return json.loads(row["result"])
        # Only native idempotent commands or reads use this helper. Model/network
        # dispatch fencing belongs to its explicit owner, never this local retry.
        result = json.loads(canonical(operation()))
        self.phases.finish(key, result)
        return result

    def _selection(self, record_id):
        item = self.runtime.observation.get_record(record_id)
        cap = 65536 if item.manifest.media_type in ("image/png", "image/jpeg") else 8192
        return {"record_id": record_id, "offset": 0, "length": min(item.manifest.byte_count, cap)}

    def _bounded_add(self, evidence, item):
        items = [value for value in evidence if value["record_id"] != item["record_id"]] + [item]
        retained, text_size, image_size, image_count = [], 0, 0, 0
        image_limit = getattr(self.student, "max_images", 1)
        for value in reversed(items):
            is_image = self.runtime.observation.get_record(value["record_id"]).manifest.media_type in ("image/png", "image/jpeg")
            if len(retained) >= 8: continue
            if is_image and image_count < image_limit and image_size + value["length"] <= 131072:
                retained.append(value); image_size += value["length"]; image_count += 1
            elif not is_image and text_size + value["length"] <= 16384:
                retained.append(value); text_size += value["length"]
        return list(reversed(retained))

    def _retain_result(self, label, result, state):
        raw = canonical({"operation": label, "result": result,
            "basis": "attributed native component artifact; not an independent observation"}).encode()
        from hashlib import sha256
        receipt = self.runtime.observe(Capture(origin_ref=self.origin.origin_ref,
            idempotency_key="component:" + digest([self.run_id, label, result]), kind="component-result",
            media_type="application/json", origin_class="generated", lineage=("C0-mediated-native-result", self.run_id, label),
            expected_bytes=len(raw), expected_sha256=sha256(raw).hexdigest()), BytesIO(raw))
        state["evidence"] = self._bounded_add(state["evidence"], self._selection(receipt.observation.record_id))
        return state

    def bootstrap(self):
        result = self.connector.call(PublicIntent(operation="mission", body={"request_id": self.run_id + ":mission"}))
        if result["http_status"] != 200:
            raise EDIError(ErrorCode.UNAVAILABLE, "original mission unavailable")
        if digest(result["body"]["mission"]) != self.connector.authority.grant.mission_sha256:
            raise EDIError(ErrorCode.INTEGRITY, "mission differs from explicitly adopted standing grant")
        return {"turn": 0, "mission": result["body"]["mission"], "evidence": [self._selection(result["evidence_record_id"])],
            "world_ids": [], "used_tokens": 0, "known_input_tokens": 0, "known_output_tokens": 0,
            "usage_unknown_jobs": 0, "state": "ready"}

    def state(self):
        row = self.journal.get("bootstrap")
        if row is None or row["state"] != "completed":
            self.journal.begin("bootstrap", {"run_id": self.run_id})
            self.journal.finish("bootstrap", self.bootstrap())
        current = json.loads(self.journal.get("bootstrap")["result"])
        for turn in range(self.max_turns):
            item = self.journal.get("turn:" + str(turn))
            if item is None: return current
            if item["state"] != "completed":
                return {**current, "state": "in-progress", "pending_turn": turn,
                    "resume_rule": "resume original phases; never replay unknown provider inference"}
            current = json.loads(item["result"])
        return ({**current, "state": "yielded", "stop_reason": "turn budget exhausted"}
                if current["state"] == "ready" else current)

    def _inquiry(self, state, inquiry_id):
        r = self.runtime
        try:
            return r.reasoning.get(inquiry_id)
        except EDIError as exc:
            if exc.code != ErrorCode.NOT_FOUND: raise
        remaining = self.max_tokens - state["used_tokens"]
        return r.reasoning.investigate(InquiryRequest.model_validate_json(canonical({
            "workspace_id": r.profile.workspace_id, "inquiry_id": inquiry_id, "request_id": inquiry_id,
            "question": state["mission"]["objective"], "purpose": state["mission"]["objective"],
            "scope": "Acquired evidence and attributed EDI artifacts; choose information and supported operations independently",
            "horizon": "Select the relevant horizon under the original mission authority", "model_revision": r.world.head(),
            "world_ids": state["world_ids"], "evidence": state["evidence"],
            "budget": Budget(rounds=4, jobs=6, input_token_cap=12288, output_token_cap=4096,
                reserved_tokens=min(remaining, 98304)).model_dump(mode="json"),
            "omitted_frontier": ["Older acquired records, derivations, C4 episodes and C3 candidates remain available through native component reads; this is a bounded cut"],
            "unknowns": ["Information not yet acquired remains unknown; generated feedback is not independent evidence"]})))

    def _receive(self, inquiry_id, action, gateway, label, trigger=None):
        r = self.runtime
        from datetime import datetime
        for attempt in range(self.max_corrections + 1):
            if utc_now() >= datetime.fromisoformat(self.deadline):
                raise EDIError(ErrorCode.CAPACITY, "persisted session deadline reached before another model job")
            key = inquiry_id + ":" + label + ":" + str(attempt)
            episode = r.reasoning.step(StepRequest(workspace_id=r.profile.workspace_id, inquiry_id=inquiry_id,
                request_id=key, action=action, reason=("Continue against the original evidence cut" if attempt == 0
                    else "Correct only the retained rejected output; retain uncertainty and original evidence"), teacher_trigger=trigger))
            job = episode.jobs[-1] if episode.jobs else None
            if episode.state == "yielded" or job is None:
                raise EDIError(ErrorCode.CAPACITY, "native inquiry job/round/token reservation exhausted")
            current = r.reasoning.get(inquiry_id)
            accepted = next((value for value in current.responses if value.job_id == job.job_id), None)
            if accepted is not None: return accepted
            rejection = next((value for value in current.rejections if value.job_id == job.job_id), None)
            if rejection is None:
                try:
                    response = r.reasoning.complete_job(job, episode)
                except ModelOutputRejected as exc:
                    receipt = exc.receipt
                except AwaitingModelResponse:
                    raise
                except EDIError as exc:
                    row = gateway.journal.get(job.job_id)
                    if row is not None and row["state"] == "pending" and row["attempts"]:
                        raise EDIError(ErrorCode.UNKNOWN_COMMIT, "Provider call remains unresolved; original inference must not be resent") from exc
                    if row is None or (row["state"] == "pending" and not row["attempts"]):
                        raise AwaitingModelAvailability(job.job_id, str(exc)) from exc
                    raise
                except (ValueError, TypeError, KeyError, UnicodeError) as exc:
                    row = gateway.journal.get(job.job_id)
                    if row is not None and row["state"] == "pending" and row["attempts"]:
                        raise EDIError(ErrorCode.UNKNOWN_COMMIT, "Provider returned an unreadable result; retain original dispatch for reconciliation") from exc
                    raise EDIError(ErrorCode.INVALID, str(exc)[:4096]) from exc
                else:
                    # Separate content validation from capacity/storage faults in
                    # the subsequent owner commit. A commit error is not a bad answer.
                    try:
                        r.reasoning.validate_response(response)
                    except EDIError as exc:
                        receipt = gateway.receipt(job.job_id)
                        if receipt is None: raise
                        receipt = {**receipt, "diagnostic": str(exc)[:8192]}
                    else:
                        r.reasoning.import_response(response)
                        return response
                rejection = RejectedResponse(workspace_id=r.profile.workspace_id, inquiry_id=inquiry_id,
                    request_id=key + ":rejected", job_id=job.job_id, raw_record_id=receipt["raw_record_id"],
                    context_sha256=job.context_sha256, diagnostic=receipt["diagnostic"],
                    input_tokens=receipt.get("input_tokens"), output_tokens=receipt.get("output_tokens"))
                r.reasoning.reject_response(rejection)
            if ((rejection.input_tokens is not None and rejection.input_tokens > job.input_token_cap) or
                    (rejection.output_tokens is not None and rejection.output_tokens > job.output_token_cap)):
                raise EDIError(ErrorCode.CAPACITY, "provider usage exceeded the original cap; no correction dispatched")
        raise EDIError(ErrorCode.INVALID, "bounded output correction exhausted; rejected originals retained")

    def _retain_candidates(self, response, state):
        if response.candidates:
            receipt = self.runtime.reasoning.submit(SubmissionRequest(workspace_id=self.runtime.profile.workspace_id,
                inquiry_id=response.inquiry_id, request_id="candidate:" + response.response_id,
                response_id=response.response_id, reason="Retain attributed candidates without automatic admission"))
            state["world_ids"] = list(dict.fromkeys(state["world_ids"] + list(receipt.changed_ids)))[-16:]
        episode = self.runtime.reasoning.get(response.inquiry_id)
        pending = tuple(item.message_id for item in episode.outbox if item.status == "pending")
        if pending:
            # Receipt acknowledges delivery of proposals only, never their
            # execution, source acquisition, truth or operational adoption.
            self.runtime.reasoning.acknowledge_outbox(OutboxAck(workspace_id=self.runtime.profile.workspace_id,
                inquiry_id=response.inquiry_id, request_id="outbox:" + digest([response.inquiry_id, pending]),
                message_ids=pending, disposition="C0 retained proposals for explicit scheduling; no execution, acquisition or admission implied"))
        return state

    def _account(self, state, inquiry_id):
        episode = self.runtime.reasoning.get(inquiry_id)
        returned = {value.job_id: value for value in (*episode.responses, *episode.rejections)}
        charged = known_in = known_out = unknown = 0
        for job in episode.jobs:
            value = returned.get(job.job_id)
            if value is None:
                # An unresolved dispatched call is never assumed free.
                charged += job.input_token_cap + job.output_token_cap
                unknown += 1
                continue
            known_in += value.input_tokens or 0
            known_out += value.output_tokens or 0
            unknown += int(value.input_tokens is None or value.output_tokens is None)
            charged += (value.input_tokens if value.input_tokens is not None else job.input_token_cap)
            charged += (value.output_tokens if value.output_tokens is not None else job.output_token_cap)
        return {**state, "used_tokens": state["used_tokens"] + charged,
            "known_input_tokens": state["known_input_tokens"] + known_in,
            "known_output_tokens": state["known_output_tokens"] + known_out,
            "usage_unknown_jobs": state["usage_unknown_jobs"] + unknown,
            "usage_basis": "known reported counts plus full reservation for unknown usage; not an energy/cost measurement"}

    def step(self):
        if not self.lock.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "C0 investigation already running")
        try:
            return self._step()
        finally:
            self.lock.release()

    def _step(self):
        from datetime import datetime
        state = self.state()
        if state["state"] not in ("ready", "in-progress"): return state
        state = {key: value for key, value in state.items() if key not in ("pending_turn", "resume_rule")}
        state["state"] = "ready"
        turn = state["turn"]
        if utc_now() >= datetime.fromisoformat(self.deadline):
            return {**state, "state": "yielded", "stop_reason": "persisted session deadline reached; pending jobs remain inspectable"}
        if state["used_tokens"] + 16384 > self.max_tokens:
            return {**state, "state": "yielded", "stop_reason": "remaining token budget cannot admit another job"}
        key, inquiry_id = "turn:" + str(turn), self.run_id + ":inquiry:" + str(turn)
        self.journal.begin(key, state, reserve_bytes=4 * 1024**2)
        self._inquiry(state, inquiry_id)
        next_state = {**state, "turn": turn + 1}
        try:
            response = self._receive(inquiry_id, "student", self.student, "student")
            next_state = self._retain_candidates(response, next_state)
            if response.operation_proposals and response.operation_proposals[0].operation == "teacher-review":
                if self.teacher is None:
                    raise EDIError(ErrorCode.UNAVAILABLE, "teacher review requested but no teacher is configured")
                trigger = response.operation_proposals[0].arguments["trigger"]
                self._receive(inquiry_id, "teacher", self.teacher, "teacher", trigger)
                response = self._receive(inquiry_id, "student", self.student, "revision")
                next_state = self._retain_candidates(response, next_state)
            if not response.operation_proposals:
                next_state.update(state="yielded", stop_reason="Student supplied no next operation; uncertainty retained")
            elif response.operation_proposals[0].operation == "teacher-review":
                next_state.update(state="yielded", stop_reason="One selective teacher cycle per turn; repeated escalation retained")
            else:
                proposal = response.operation_proposals[0]
                next_state["last_response_id"] = response.response_id
                result = self._phase(key + ":dispatch", proposal, lambda: self._dispatch_known(proposal, next_state, inquiry_id))
                next_state = result
            episode = self.runtime.reasoning.get(inquiry_id)
            # Carry actual student revision and attributed critique into the next
            # bounded context. The complete episode remains in its native C4 store.
            memory = {"inquiry_id": inquiry_id, "sequence": episode.sequence,
                "student_revision": response.model_dump(mode="json"),
                "teacher_feedback": [value.model_dump(mode="json") for value in episode.responses
                    if next(j for j in episode.jobs if j.job_id == value.job_id).role == "teacher"]}
            next_state = self._retain_result("reasoning-memory", memory, next_state)
        except AwaitingModelAvailability as exc:
            return {**state, "state": "waiting-model", "job_id": exc.job_id,
                "inquiry_id": inquiry_id, "error": exc.as_dict(),
                "resume_rule": "Original job has no recorded provider dispatch; restore its configured dependency and resume"}
        except AwaitingModelResponse as exc:
            return {**state, "state": "waiting-teacher", "job_id": exc.job_id, "request_path": exc.request_path,
                "inquiry_id": inquiry_id, "resume_rule": "Import feedback, then resume this original turn"}
        except EDIError as exc:
            if exc.code in (ErrorCode.UNKNOWN_COMMIT, ErrorCode.STORAGE):
                return {**state, "state": "uncertain-completion", "inquiry_id": inquiry_id, "error": exc.as_dict()}
            next_state.update(state="yielded", stop_reason=str(exc), error=exc.as_dict())
        next_state = self._account(next_state, inquiry_id)
        self.journal.finish(key, next_state)
        return next_state

    def _dispatch_known(self, proposal, state, inquiry_id):
        def unresolved_broker():
            if proposal.operation != "world-call": return False
            row = self.connector.journal.get("c0:" + digest([self.run_id, state["turn"], proposal]))
            return row is not None and row["state"] == "pending" and bool(row["attempts"])
        try:
            return self._dispatch(proposal, state, inquiry_id)
        except EDIError as exc:
            if exc.code in (ErrorCode.UNKNOWN_COMMIT, ErrorCode.STORAGE): raise
            if unresolved_broker():
                raise EDIError(ErrorCode.UNKNOWN_COMMIT, "Original public operation has no committed receipt; reconcile its original request") from exc
            return self._retain_result(proposal.operation + ":error", exc.as_dict(), state)
        except (ValidationError, ValueError, TypeError, KeyError) as exc:
            if unresolved_broker():
                raise EDIError(ErrorCode.UNKNOWN_COMMIT, "Public operation returned an unreadable result; retain its original request") from exc
            error = EDIError(ErrorCode.INVALID, str(exc)[:4096])
            return self._retain_result(proposal.operation + ":error", error.as_dict(), state)

    def _dispatch(self, proposal, state, inquiry_id):
        from datetime import datetime
        if utc_now() >= datetime.fromisoformat(self.deadline):
            raise EDIError(ErrorCode.CAPACITY, "persisted session deadline reached before operation dispatch")
        from edi.inquiry.operations import invoke
        r, arguments = self.runtime, proposal.arguments
        command = "c0:" + digest([self.run_id, state["turn"], proposal])
        if proposal.operation == "world-call":
            intent = PublicIntent.model_validate_json(canonical(arguments))
            result = self.connector.call(PublicIntent(operation=intent.operation,
                body={**intent.body, "request_id": command}))
            state["evidence"] = self._bounded_add(state["evidence"], self._selection(result["evidence_record_id"]))
            decoded = r.interpretation.interpret(InterpretRequest(workspace_id=r.profile.workspace_id,
                request_id=inquiry_id + ":decode", inputs=(InputSpec(record_id=result["evidence_record_id"]),)))
            state = self._retain_result("interpret", decoded, state)
            state["last_public_result"] = result
            if intent.operation == "submit" and result["http_status"] == 200:
                state.update(state="completed", stop_reason="Student submitted a final report")
        elif proposal.operation == "acquire-asset":
            observation = self.connector.acquire_asset(arguments["document_id"], command)
            state["evidence"] = self._bounded_add(state["evidence"], self._selection(observation.record_id))
        elif proposal.operation == "select-context":
            selected = tuple(EvidenceSelection.model_validate_json(canonical(x)) for x in arguments["evidence"])
            for item in selected:
                source = r.observation.get_record(item.record_id)
                if source.scope_id != r.profile.workspace_id or item.offset + item.length > source.manifest.byte_count:
                    raise EDIError(ErrorCode.DENIED, "selected context exceeds acquired workspace/range")
            state.update(evidence=[x.model_dump(mode="json") for x in selected], world_ids=arguments["world_ids"])
        elif proposal.operation in ("analysis-compile", "analysis-run", "component-call"):
            if proposal.operation == "component-call":
                operation, data = arguments["operation"], arguments["arguments"]
            else:
                # Backwards-compatible envelope; C0 still owns command identity.
                operation = proposal.operation
                if arguments["workspace_id"] != r.profile.workspace_id:
                    raise EDIError(ErrorCode.DENIED, "analysis workspace differs")
                data = {key: value for key, value in arguments.items() if key not in ("workspace_id", "request_id")}
            episode = r.reasoning.get(inquiry_id)
            response = next(value for value in episode.responses if value.response_id == state["last_response_id"])
            assistance = {"response_id": response.response_id, "lineage": [inquiry_id, response.response_id, response.context_sha256],
                "provenance": {"producer": "C4", "model_or_checkpoint": response.binding.revision,
                    "prompt_version": "meadows-inquiry/1.0", "tool_schema_version": "edi-native-operations/1.2",
                    "configuration": {"binding": response.binding.model_dump(mode="json"), "response_id": response.response_id}}}
            result = invoke(r, operation, data, command, assistance=assistance)
            commit = result if operation == "interpret-submit" else getattr(result, "commit", None)
            if commit is not None and hasattr(commit, "changed_ids"):
                state["world_ids"] = list(dict.fromkeys(state["world_ids"] + list(commit.changed_ids)))[-16:]
            state = self._retain_result(operation, result, state)
        elif proposal.operation == "yield":
            state.update(state="yielded", stop_reason=arguments.get("reason", "Student yielded"))
        else:
            raise EDIError(ErrorCode.UNSUPPORTED, "operation is not connected to a C0 native port")
        return state
