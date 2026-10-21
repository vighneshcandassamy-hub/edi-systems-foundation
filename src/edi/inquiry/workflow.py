"""Bounded C0 orchestration over existing owner ports; no native model call."""
from contextlib import contextmanager
from hashlib import sha256
from io import BytesIO
import json
from threading import BoundedSemaphore
from time import monotonic

from pydantic import ValidationError

from edi.inquiry.contracts import WorkflowInput, WorkflowOperatorInput, WorkflowSpec, WorkflowStatus
from edi.inquiry.sqlite import canonical
from edi.shared.contracts import utc_now
from edi.shared.errors import EDIError, ErrorCode

OPERATORS = frozenset(("world-commit", "agency-adopt", "agency-reconcile", "agency-access-disposition", "analysis-control"))


class MissingInput(Exception):
    def __init__(self, input_id): self.input_id = input_id


def pointer_tokens(path):
    if not isinstance(path, str) or len(path) > 2048 or (path and not path.startswith("/")):
        raise EDIError(ErrorCode.INVALID, "workflow selector must be a bounded JSON pointer")
    if not path: return ()
    tokens = path[1:].split("/")
    if len(tokens) > 32: raise EDIError(ErrorCode.CAPACITY, "workflow selector depth exceeded")
    decoded = []
    for raw in tokens:
        # Only RFC 6901 escapes; unsupported syntax never becomes Python indexing.
        if "~" in raw.replace("~0", "").replace("~1", ""):
            raise EDIError(ErrorCode.INVALID, "invalid JSON pointer escape")
        decoded.append(raw.replace("~1", "/").replace("~0", "~"))
    return tuple(decoded)


def pointer(value, path):
    for token in pointer_tokens(path):
        if isinstance(value, dict) and token in value: value = value[token]
        elif isinstance(value, list) and token.isascii() and token.isdecimal() and str(int(token)) == token and int(token) < len(value): value = value[int(token)]
        else: raise EDIError(ErrorCode.NOT_FOUND, "workflow JSON selector unavailable")
    return value


class Workflow:
    def __init__(self, runtime, profile, store):
        self.runtime, self.profile, self._store = runtime, profile, store
        self._slot = BoundedSemaphore(1)

    @contextmanager
    def _admit(self):
        if not self._slot.acquire(blocking=False): raise EDIError(ErrorCode.CAPACITY, "C0 workflow runner busy", retryable=True)
        try: yield
        finally: self._slot.release()

    def _scope(self, request):
        if request.workspace_id != self.profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C0 workflow workspace differs")

    def _operator(self, operation):
        if operation in OPERATORS and not self.profile.trusted_operator_steps:
            raise EDIError(ErrorCode.DENIED, "operator admission/adoption/reconciliation step disabled in this C0 profile")

    @staticmethod
    def _walk(value, visit, depth=0):
        if depth > 32: raise EDIError(ErrorCode.CAPACITY, "workflow template depth exceeded")
        if isinstance(value, dict):
            if "$step" in value or "$input" in value:
                key = "$step" if "$step" in value else "$input"
                if set(value) != {key, "path"} or not isinstance(value[key], str) or not 1 <= len(value[key]) <= 256:
                    raise EDIError(ErrorCode.INVALID, "invalid workflow reference shape")
                pointer_tokens(value["path"])
                visit(key, value[key])
            else:
                for item in value.values(): Workflow._walk(item, visit, depth + 1)
        elif isinstance(value, list):
            for item in value: Workflow._walk(item, visit, depth + 1)

    def create(self, spec: WorkflowSpec):
        spec = WorkflowSpec.model_validate_json(canonical(spec))
        self._scope(spec)
        prior = set()
        for step in spec.steps:
            self._operator(step.operation)
            for condition in step.require: pointer_tokens(condition.path)
            if step.operation in OPERATORS and (set(step.arguments) != {"$input", "path"} or step.arguments.get("path") != ""):
                raise EDIError(ErrorCode.DENIED, "operator steps require a whole explicit operator-decision input, never computed model output")
            def visit(kind, key):
                if kind == "$step" and key not in prior:
                    raise EDIError(ErrorCode.INVALID, "workflow may reference only an earlier step")
            self._walk(step.arguments, visit)
            prior.add(step.step_id)
        self._store.create(spec)
        return self.status(spec.workflow_id)

    def supply(self, request: WorkflowInput):
        request = WorkflowInput.model_validate_json(canonical(request))
        self._scope(request)
        if request.authority != "data" or request.operator_id is not None:
            raise EDIError(ErrorCode.DENIED, "ordinary workflow input cannot supply operator authority")
        self._store.load(request.workflow_id)
        self._store.supply(request)
        return self.status(request.workflow_id)

    def supply_operator(self, request: WorkflowOperatorInput):
        """Separate trusted-local operator API; labels still do not authenticate a person."""
        request = WorkflowOperatorInput.model_validate_json(canonical(request))
        self._scope(request)
        if not self.profile.trusted_operator_steps or request.operator_id not in self.profile.operator_ids:
            raise EDIError(ErrorCode.DENIED, "operator workflow input is not enabled for this configured operator")
        self._store.load(request.workflow_id)
        self._store.supply(request)
        return self.status(request.workflow_id)

    def output(self, workflow_id, step_id):
        self._store.load(workflow_id)
        return self._store.selected(workflow_id, "result", step_id)

    def attempts(self, workflow_id, step_id, *, after=0, limit=25):
        self._store.load(workflow_id)
        return self._store.attempts(workflow_id, step_id, after=after, limit=limit)

    def _resolve(self, value, workflow_id, inputs, steps):
        size = 0
        def charge(item):
            nonlocal size
            size += len(canonical(item).encode("utf-8"))
            if size > self.profile.max_step_bytes:
                raise EDIError(ErrorCode.CAPACITY, "workflow resolved-reference budget exceeded")
            return item
        def resolve(item, depth=0):
            if depth > 32: raise EDIError(ErrorCode.CAPACITY, "workflow reference depth exceeded")
            if isinstance(item, dict):
                if "$input" in item:
                    if item["$input"] not in inputs: raise MissingInput(item["$input"])
                    return charge(pointer(self._store.selected(workflow_id, "input", item["$input"]), item["path"]))
                if "$step" in item:
                    if steps.get(item["$step"], {}).get("state") != "completed":
                        raise EDIError(ErrorCode.CONFLICT, "workflow reference is not a committed step")
                    return charge(pointer(self._store.selected(workflow_id, "result", item["$step"]), item["path"]))
                return {key: resolve(child, depth + 1) for key, child in item.items()}
            if isinstance(item, list): return [resolve(child, depth + 1) for child in item]
            return charge(item)
        result = resolve(value)
        if len(canonical(result).encode("utf-8")) > self.profile.max_step_bytes:
            raise EDIError(ErrorCode.CAPACITY, "workflow resolved arguments too large")
        return result

    def status(self, workflow_id):
        raw, digest, inputs, steps, cancelled = self._store.load(workflow_id)
        spec = WorkflowSpec.model_validate_json(canonical(raw))
        complete = tuple(s.step_id for s in spec.steps if steps.get(s.step_id, {}).get("state") == "completed")
        next_step = next((s for s in spec.steps if s.step_id not in complete), None)
        state, waiting, error = "ready", None, None
        if cancelled: state = "cancelled"
        elif next_step is None: state = "completed"
        else:
            item = steps.get(next_step.step_id)
            if item and item["state"] == "pending": state = "uncertain-completion"
            elif item and item["state"] == "failed": state, error = "failed", item["error"]
            else:
                try: self._resolve(next_step.arguments, workflow_id, inputs, steps)
                except MissingInput as exc: state, waiting = "waiting-input", exc.input_id
                except EDIError as exc: state, error = "failed", exc.as_dict()
        # Compact metadata, not every potentially large output/argument document.
        return WorkflowStatus(workspace_id=self.profile.workspace_id, workflow_id=workflow_id, state=state,
            completed_steps=complete, next_step=next_step.step_id if next_step else None,
            waiting_input=waiting, error=error, outputs=steps, plan_sha256=digest)

    def cancel(self, workflow_id):
        self._store.load(workflow_id)
        self._store.cancel(workflow_id)
        return self.status(workflow_id)

    def resume(self, workflow_id, *, retry_uncertain=False):
        with self._admit():
            if retry_uncertain and not self.profile.trusted_operator_steps:
                raise EDIError(ErrorCode.DENIED, "uncertain-step retry requires trusted local reconciliation profile")
            started = monotonic()
            while monotonic() - started < self.profile.max_resume_seconds:
                status = self.status(workflow_id)
                if status.state not in ("ready", "uncertain-completion"): return status
                if status.state == "uncertain-completion" and not retry_uncertain: return status
                raw, _, inputs, steps, _ = self._store.load(workflow_id)
                spec = WorkflowSpec.model_validate_json(canonical(raw))
                step = next(s for s in spec.steps if s.step_id == status.next_step)
                self._operator(step.operation)
                if status.state == "uncertain-completion":
                    arguments = self._store.selected(workflow_id, "arguments", step.step_id)
                else:
                    arguments = self._resolve(step.arguments, workflow_id, inputs, steps)
                if step.operation in OPERATORS:
                    approval = self._store.selected(workflow_id, "input-record", step.arguments["$input"])
                    if approval["authority"] != "operator-decision" or approval["operator_id"] not in self.profile.operator_ids:
                        raise EDIError(ErrorCode.DENIED, "operator step does not have an explicit operator-decision record")
                    if "operator_id" in arguments and arguments["operator_id"] != approval["operator_id"]:
                        raise EDIError(ErrorCode.DENIED, "native decision operator differs from C0 approval attribution")
                attempt = self._store.begin(workflow_id, step.step_id, arguments, retry_uncertain=retry_uncertain)
                retry_uncertain = False
                if attempt is None: return self.status(workflow_id)
                tick = monotonic()
                result, error = None, None
                try:
                    result = json.loads(canonical(self._invoke(workflow_id, step, arguments)))
                    if len(canonical(result).encode("utf-8")) > self.profile.max_step_bytes:
                        # Owner result may already exist; preserve uncertainty instead of repeating work.
                        raise EDIError(ErrorCode.UNKNOWN_COMMIT, "native result exceeds C0 result budget; inspect the owner artifact before retry")
                    for condition in step.require:
                        if canonical(pointer(result, condition.path)) != canonical(condition.equals):
                            raise EDIError(ErrorCode.INCOMPLETE, "native step returned but a declared downstream acceptance condition was not met")
                except EDIError as exc:
                    if exc.code in (ErrorCode.UNKNOWN_COMMIT, ErrorCode.STORAGE):
                        # A failing transport/storage acknowledgement cannot establish nonexecution.
                        return self.status(workflow_id)
                    error = exc.as_dict()
                except (ValidationError, ValueError, TypeError, KeyError) as exc:
                    error = EDIError(ErrorCode.INVALID, str(exc)[:4096]).as_dict()
                self._store.finish(workflow_id, step.step_id, attempt, result, error, monotonic() - tick)
                if error: return self.status(workflow_id)
            return self.status(workflow_id).model_copy(update={"state": "yielded"})

    def _invoke(self, workflow_id, step, arguments):
        from edi.agency import contracts as agency
        from edi.analyze import contracts as analyze
        from edi.assess import contracts as assess
        from edi.interpret import contracts as interpret
        from edi.observe.contracts import Capture, OriginSpec
        from edi.reason import contracts as reason
        from edi.world.contracts import WorldCursor, WorldPatch, WorldQuery

        key = "c0:" + sha256((workflow_id + "\x00" + step.step_id).encode("utf-8")).hexdigest()
        data = dict(arguments)
        def call(cls, method):
            fields = cls.model_fields
            if "workspace_id" in fields: data.setdefault("workspace_id", self.profile.workspace_id)
            if "request_id" in fields: data.setdefault("request_id", key)
            request = cls.model_validate_json(canonical(data))
            if hasattr(request, "workspace_id"): self._scope(request)
            return method(request)
        op, runtime = step.operation, self.runtime
        if op == "register-origin": return call(OriginSpec, runtime.register_origin)
        if op in ("observe-json", "observe-bytes"):
            key_name = "payload" if op == "observe-json" else "payload_base64"
            if set(data) != {"capture", key_name}: raise EDIError(ErrorCode.INVALID, "observation requires capture and its one declared payload field only")
            if op == "observe-json": payload = canonical(data["payload"]).encode("utf-8")
            else:
                from base64 import b64decode
                encoded = data["payload_base64"]
                if not isinstance(encoded, str): raise EDIError(ErrorCode.INVALID, "native bytes require a base64 string")
                limit = min(self.profile.max_step_bytes, runtime.profile.max_record_bytes)
                if len(encoded) > 4 * ((limit + 2) // 3): raise EDIError(ErrorCode.CAPACITY, "workflow native byte payload exceeds finite adapter limit")
                payload = b64decode(encoded, validate=True)
                if len(payload) > limit: raise EDIError(ErrorCode.CAPACITY, "workflow native bytes exceed payload limit")
            capture = dict(data["capture"])
            capture.setdefault("idempotency_key", key)
            capture.setdefault("media_type", "application/json" if op == "observe-json" else "application/octet-stream")
            capture.setdefault("expected_bytes", len(payload))
            capture.setdefault("expected_sha256", sha256(payload).hexdigest())
            return runtime.observe(Capture.model_validate_json(canonical(capture)), BytesIO(payload))
        if op == "coverage":
            if data: raise EDIError(ErrorCode.INVALID, "coverage has no arguments")
            return runtime.observation.coverage()
        if op == "interpret": return call(interpret.InterpretRequest, runtime.interpretation.interpret)
        if op == "interpret-get": return runtime.interpretation.get_derivation(**data)
        if op == "interpret-submit":
            data.setdefault("world_request_id", key)
            return call(interpret.SubmissionRequest, runtime.interpretation.submit)
        if op in ("world-propose", "world-commit"):
            self._operator(op)
            data.setdefault("proposer", "C0")
            if data["proposer"] != "C0": raise EDIError(ErrorCode.DENIED, "C0 cannot impersonate a component proposer")
            return call(WorldPatch, runtime.world.commit if op == "world-commit" else runtime.world_for("C0").propose_patch)
        if op == "world-get": return runtime.world_for("C0").get(**data)
        if op == "world-query":
            if data.get("query") is not None: data["query"] = WorldQuery.model_validate_json(canonical(data["query"]))
            if data.get("cursor") is not None: data["cursor"] = WorldCursor.model_validate_json(canonical(data["cursor"]))
            return runtime.world_for("C0").query(**data)
        if op == "world-dependencies": return runtime.world_for("C0").dependencies(**data)
        if op == "world-status": return runtime.world_for("C0").commit_status(**data)
        if op == "world-head":
            if data: raise EDIError(ErrorCode.INVALID, "world-head has no arguments")
            return {"revision": runtime.world.head()}
        if op == "world-ack": return {"position": runtime.acknowledge_world_progress(**data)}
        if op == "reason-export": return runtime.reasoning.export_job(**data)
        if op == "reason-get": return runtime.reasoning.get(**data)
        if op == "reason-rank": return runtime.reasoning.rank_frontier(**data)
        if op == "reason-assessments":
            if data.get("cursor") is not None: data["cursor"] = assess.ArtifactCursor.model_validate_json(canonical(data["cursor"]))
            return runtime.reasoning.query_assessments(**data)
        if op == "analysis-status": return runtime.analysis.status(**data)
        if op == "analysis-get": return runtime.analysis.get_run(**data)
        if op == "agency-policy": return runtime.agency_for("C0").read_policy(**data)
        if op == "agency-receipt": return runtime.agency_for("C0").get_receipt(**data)
        if op == "assess-query":
            if data.get("cursor") is not None: data["cursor"] = assess.ArtifactCursor.model_validate_json(canonical(data["cursor"]))
            return runtime.assessment.query(**data)
        if op == "assess-get":
            if set(data) != {"kind", "artifact_id"}: raise EDIError(ErrorCode.INVALID, "assessment read requires kind and artifact_id only")
            methods = {"forecast": runtime.assessment.get_forecast, "comparison": runtime.assessment.get_comparison,
                "review": runtime.assessment.get_review, "finding": runtime.assessment.get_finding}
            if data["kind"] not in methods: raise EDIError(ErrorCode.UNSUPPORTED, "unsupported assessment artifact kind")
            return methods[data["kind"]](data["artifact_id"])
        if op == "deliver-finding":
            if set(data) != {"finding_id"}: raise EDIError(ErrorCode.INVALID, "delivery requires a finding ID only")
            finding = runtime.assessment.get_finding(data["finding_id"])
            if finding.request.expiry <= utc_now(): raise EDIError(ErrorCode.DENIED, "finding expired before delivery")
            return {"finding_id": data["finding_id"], "finding_sha256": finding.artifact_sha256,
                "channel": "C0-internal-workflow-result", "delivered_at": utc_now().isoformat(),
                "finding": finding.model_dump(mode="json"), "external_message_sent": False}
        # Select the owner lazily; observation-only plans never open other owner stores.
        if op.startswith("reason-"):
            owner = runtime.reasoning
            options = {"reason-investigate": (reason.InquiryRequest, owner.investigate),
                "reason-step": (reason.StepRequest, owner.step), "reason-import": (reason.Response, owner.import_response),
                "reason-submit": (reason.SubmissionRequest, owner.submit), "reason-frontier": (reason.FrontierUpdate, owner.update_frontier),
                "reason-ack": (reason.OutboxAck, owner.acknowledge_outbox)}
        elif op.startswith("analysis-"):
            owner = runtime.analysis
            options = {"analysis-compile": (analyze.CompileRequest, owner.compile), "analysis-run": (analyze.RunRequest, owner.run_scenario),
                "analysis-control": (analyze.RunControl, owner.control_run)}
        elif op.startswith("assess-"):
            owner = runtime.assessment
            options = {"assess-seal": (assess.SealRequest, owner.seal_forecast), "assess-compare": (assess.CompareRequest, owner.compare_outcome),
                "assess-review": (assess.ReviewRequest, owner.review_revision), "assess-finding": (assess.FindingRequest, owner.draft_finding),
                "assess-yield": (assess.YieldRequest, owner.review_inquiry_yield), "assess-submit": (assess.SubmissionRequest, owner.submit_revision)}
        elif op.startswith("agency-"):
            owner = runtime.agency
            options = {"agency-propose": (agency.AmendmentRequest, owner.request_adoption), "agency-adopt": (agency.AdoptionRequest, owner.decide_adoption),
                "agency-check": (agency.ActionRequest, owner.check_action), "agency-dispatch": (agency.DispatchRequest, owner.dispatch_authorized),
                "agency-access": (agency.AccessRequest, owner.review_access_scope), "agency-actor-view": (agency.ActorViewRequest, owner.qualify_actor_view),
                "agency-archive": (agency.ReportRequest, owner.archive_report), "agency-reconcile": (agency.ReconcileRequest, owner.reconcile_execution),
                "agency-access-disposition": (agency.AccessDispositionRequest, owner.record_access_disposition),
                "agency-submit": (agency.ModelUpdateRequest, owner.submit_model_update)}
        else: raise EDIError(ErrorCode.UNSUPPORTED, "unallocated C0 workflow operation")
        if op not in options: raise EDIError(ErrorCode.UNSUPPORTED, "unsupported workflow operation")
        self._operator(op)
        cls, method = options[op]
        return call(cls, method)
