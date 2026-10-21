"""C0 generic resumable investigator. Domain choices come from native C4 responses."""
import json
from time import monotonic

from edi.agency.benchmark import PublicIntent
from edi.interpret.contracts import InputSpec, InterpretRequest
from edi.reason.contracts import Budget, EvidenceSelection, InquiryRequest, StepRequest, SubmissionRequest
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class Investigation:
    """One immutable turn intent at a time; no domain rules or source-priority list.

    A new turn takes a fresh cut. Exact selected context is explicit. New acquired
    result plus the previous cut are the default continuation, with omitted older
    records retained in C1. Model can select any acquired evidence/C3 candidate.
    This source increment does not enable objective adoption or C3 promotion.
    """
    def __init__(self, runtime, connector, student_gateway, path, run_id, *, teacher_gateway=None,
                 max_turns=32, max_tokens=262144, session_seconds=3600):
        self.runtime, self.connector = runtime, connector
        self.student, self.teacher = student_gateway, teacher_gateway
        self.run_id, self.max_turns, self.max_tokens = run_id, max_turns, max_tokens
        self.session_seconds, self.started = session_seconds, monotonic()
        self.journal = CallJournal(path, "investigation_c0", max_calls=max_turns + 2, max_bytes=256 * 1024**2)
        self.journal.begin("configuration", {"run_id": run_id, "session_id": connector.session_id,
            "workspace": runtime.profile.workspace_id, "student": student_gateway.binding.model_dump(mode="json"),
            "teacher": teacher_gateway.binding.model_dump(mode="json") if teacher_gateway else None,
            "max_turns": max_turns, "max_tokens": max_tokens})
        self.journal.finish("configuration", {"frozen": True})

    def _selection(self, record_id):
        item = self.runtime.observation.get_record(record_id)
        return {"record_id": record_id, "offset": 0, "length": min(item.manifest.byte_count, 8192)}

    @staticmethod
    def _bounded_add(evidence, item):
        # Pure byte/recency allocation, no topic/relevance/causal selection.
        items = evidence + [item]
        retained, size = [], 0
        for value in reversed(items):
            if size + value["length"] <= 16384 and len(retained) < 8:
                retained.append(value); size += value["length"]
        return list(reversed(retained))

    def bootstrap(self):
        result = self.connector.call(PublicIntent(operation="mission", body={"request_id": self.run_id + ":mission"}))
        if result["http_status"] != 200:
            raise EDIError(ErrorCode.UNAVAILABLE, "original mission unavailable")
        if digest(result["body"]["mission"]) != self.connector.authority.grant.mission_sha256:
            raise EDIError(ErrorCode.INTEGRITY, "public mission differs from explicitly adopted standing grant")
        return {"turn": 0, "mission": result["body"]["mission"], "evidence": [self._selection(result["evidence_record_id"])],
            "world_ids": [], "used_tokens": 0, "state": "ready"}

    def state(self):
        previous = self.journal.get("bootstrap")
        if previous is None:
            self.journal.begin("bootstrap", {"run_id": self.run_id})
            self.journal.finish("bootstrap", self.bootstrap())
        current = json.loads(self.journal.get("bootstrap")["result"])
        for turn in range(self.max_turns):
            item = self.journal.get("turn:" + str(turn))
            if item is None:
                return current
            if item["state"] != "completed":
                return {**current, "state": "uncertain-completion", "pending_turn": turn}
            current = json.loads(item["result"])
        return {**current, "state": "yielded", "stop_reason": "turn budget exhausted"}

    def step(self):
        state = self.state()
        if state["state"] != "ready":
            return state
        allowance = 49152 if self.teacher is not None else 16384
        if monotonic() - self.started >= self.session_seconds or state["used_tokens"] + allowance > self.max_tokens:
            return {**state, "state": "yielded", "stop_reason": "wall-time or token budget; durable state retained"}
        turn, r = state["turn"], self.runtime
        if turn >= self.max_turns:
            return {**state, "state": "yielded", "stop_reason": "turn budget"}
        key, inquiry_id = "turn:" + str(turn), self.run_id + ":inquiry:" + str(turn)
        self.journal.begin(key, state, reserve_bytes=4 * 1024**2)
        if not self.journal.claim_once(key):
            raise EDIError(ErrorCode.UNKNOWN_COMMIT, "investigation turn already dispatched; inspect original owner artifacts")
        budget = Budget(input_token_cap=12288, output_token_cap=4096, reserved_tokens=65536)
        inquiry = InquiryRequest.model_validate_json(canonical({"workspace_id": r.profile.workspace_id,
            "inquiry_id": inquiry_id, "request_id": inquiry_id, "question": state["mission"]["objective"],
            "purpose": state["mission"]["objective"], "scope": "Acquired public evidence and candidate EDI representations; choose additional information through available public operations",
            "horizon": "Choose the relevant horizon within original district authority", "model_revision": r.world.head(),
            "world_ids": state["world_ids"], "evidence": state["evidence"], "budget": budget.model_dump(mode="json"),
            "omitted_frontier": ["Older acquired records remain in C1; this is a bounded cut, not the full archive"],
            "unknowns": ["Information not yet acquired remains unknown"]}))
        episode = r.reasoning.investigate(inquiry)
        episode = r.reasoning.step(StepRequest(workspace_id=r.profile.workspace_id, inquiry_id=inquiry_id,
            request_id=inquiry_id + ":student", action="student", reason="Continue the original objective using current evidence"))
        job = episode.jobs[-1]
        response = self.student.complete(job, episode)
        r.reasoning.import_response(response)
        next_state = {**state, "turn": turn + 1, "used_tokens": state["used_tokens"] + response.input_tokens + response.output_tokens}
        if response.candidates:
            receipt = r.reasoning.submit(SubmissionRequest(workspace_id=r.profile.workspace_id, inquiry_id=inquiry_id,
                request_id=inquiry_id + ":candidates", response_id=response.response_id, reason="Retain student candidates without promotion"))
            next_state["world_ids"] = list(dict.fromkeys(state["world_ids"] + list(receipt.changed_ids)))[-16:]
        if not response.operation_proposals:
            next_state.update(state="yielded", stop_reason="Student supplied no next operation; retain uncertainty")
        else:
            proposal = response.operation_proposals[0]
            next_state = self._dispatch(proposal, next_state, inquiry_id)
        self.journal.finish(key, next_state)
        return next_state

    def _dispatch(self, proposal, state, inquiry_id):
        r, arguments = self.runtime, proposal.arguments
        if proposal.operation == "world-call":
            intent = PublicIntent.model_validate_json(canonical(arguments))
            # The controller assigns stable request identity only; no content choices.
            body = {**intent.body, "request_id": self.run_id + ":world:" + str(state["turn"])}
            result = self.connector.call(PublicIntent(operation=intent.operation, body=body))
            state["evidence"] = self._bounded_add(state["evidence"], self._selection(result["evidence_record_id"]))
            # Bounded native decoding is independent of interpretation/causal truth.
            r.interpretation.interpret(InterpretRequest(workspace_id=r.profile.workspace_id,
                request_id=inquiry_id + ":decode", inputs=(InputSpec(record_id=result["evidence_record_id"]),)))
            state["last_public_result"] = result
            if intent.operation == "submit" and result["http_status"] == 200:
                state.update(state="completed", stop_reason="Student submitted a final report")
        elif proposal.operation == "acquire-asset":
            if set(arguments) != {"document_id"} or not isinstance(arguments["document_id"], str):
                raise EDIError(ErrorCode.INVALID, "asset intent requires one public document ID")
            observation = self.connector.acquire_asset(arguments["document_id"], self.run_id + ":asset:" + str(state["turn"]))
            state["evidence"] = self._bounded_add(state["evidence"], self._selection(observation.record_id))
        elif proposal.operation == "select-context":
            if set(arguments) != {"evidence", "world_ids"}:
                raise EDIError(ErrorCode.INVALID, "context selection needs evidence and world IDs only")
            selected = tuple(EvidenceSelection.model_validate_json(canonical(x)) for x in arguments["evidence"])
            if len(selected) > 16 or len(arguments["world_ids"]) > 16:
                raise EDIError(ErrorCode.CAPACITY, "context selection exceeds C4 bounds")
            # Actual C1/C3 access checks also run when C4 assembles the next cut.
            for item in selected:
                if r.observation.get_record(item.record_id).scope_id != r.profile.workspace_id:
                    raise EDIError(ErrorCode.DENIED, "context crosses workspace")
            state.update(evidence=[x.model_dump(mode="json") for x in selected], world_ids=arguments["world_ids"])
        elif proposal.operation in ("analysis-compile", "analysis-run"):
            from edi.analyze.contracts import CompileRequest, RunRequest
            cls, method = (CompileRequest, r.analysis.compile) if proposal.operation == "analysis-compile" else (RunRequest, r.analysis.run_scenario)
            native = cls.model_validate_json(canonical(arguments))
            if native.workspace_id != r.profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "analysis workspace differs")
            result = method(native)
            state["last_analysis"] = result.model_dump(mode="json")
        elif proposal.operation == "teacher-review":
            if self.teacher is None:
                state.update(state="yielded", stop_reason="Selective teacher requested but unavailable")
            else:
                episode = r.reasoning.step(StepRequest.model_validate_json(canonical({"workspace_id": r.profile.workspace_id,
                    "inquiry_id": inquiry_id, "request_id": inquiry_id + ":teacher", "action": "teacher",
                    "reason": "Student selected critique", "teacher_trigger": arguments.get("trigger")})))
                critique = self.teacher.complete(episode.jobs[-1], episode)
                r.reasoning.import_response(critique)
                state["used_tokens"] += critique.input_tokens + critique.output_tokens
                # Preserve original cut and critique for the allowed second student round.
                episode = r.reasoning.step(StepRequest(workspace_id=r.profile.workspace_id, inquiry_id=inquiry_id,
                    request_id=inquiry_id + ":revision", action="student", reason="Consider attributed teacher critique against original cut"))
                revision = self.student.complete(episode.jobs[-1], episode)
                r.reasoning.import_response(revision)
                state["used_tokens"] += revision.input_tokens + revision.output_tokens
                if revision.operation_proposals and revision.operation_proposals[0].operation != "teacher-review":
                    state = self._dispatch(revision.operation_proposals[0], state, inquiry_id + ":revision")
                else:
                    state.update(state="yielded", stop_reason="No distinct next operation after critique")
        else:
            state.update(state="yielded", stop_reason=arguments.get("reason", "Student yielded"))
        return state
