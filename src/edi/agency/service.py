"""C7 research-only commands; attributed actor views never confer runtime rights."""
from contextlib import contextmanager
from datetime import timedelta
from hashlib import sha256
from io import BytesIO
from threading import BoundedSemaphore
from time import monotonic

from edi.agency.contracts import (
    AccessDisposition, AccessDispositionRequest, AccessRequest, AccessReview, AccessScope,
    ActionDecision, ActionRequest, ActorView, ActorViewRequest, Adoption, AdoptionRequest,
    Amendment, AmendmentRequest, DispatchRequest, ExecutionIntent, ExecutionReceipt,
    ExecutionStatus, ModelStage, ModelSubmission, ModelUpdateRequest, PolicyVersion,
    ReconcileRequest, ReportArchive, ReportRequest, ReportStage, SelectObservations, SelectWorld,
)
from edi.agency.sqlite import canonical
from edi.observe.contracts import Capture
from edi.shared.contracts import Capability, TemporalScope, TimeValue, utc_now
from edi.shared.errors import EDIError, ErrorCode
from edi.world.contracts import Put, WorldPatch

IMPLEMENTATION = "edi-c7/0.8.0"


def parsed(cls, document): return cls.model_validate_json(canonical(document))


def digest(record):
    return sha256(canonical(record.model_copy(update={"artifact_sha256": ""})).encode("utf-8")).hexdigest()


def stamped(record): return record.model_copy(update={"artifact_sha256": digest(record)})


def verified(cls, document):
    value = parsed(cls, document)
    if value.artifact_sha256 != digest(value):
        raise EDIError(ErrorCode.INTEGRITY, "C7 retained artifact hash differs")
    return value


class AgencyAccess:
    """C0 request/result lane; operator adoption/reconciliation is deliberately absent."""
    def __init__(self, service): self._service = service
    def check_action(self, request): return self._service.check_action(request)
    def request_adoption(self, request): return self._service.request_adoption(request)
    def dispatch_authorized(self, request): return self._service.dispatch_authorized(request)
    def review_access_scope(self, request): return self._service.review_access_scope(request)
    def read_policy(self, revision=None): return self._service.read_policy(revision)
    def get_receipt(self, execution_id): return self._service.get_receipt(execution_id)


class Agency:
    capability = Capability(owner="C7", functions=("F70", "F71", "F72", "F73"),
        state="implemented-unqualified", details="Partial C7: attributed information masks, explicit local policy adoption, scoped internal reads, durable command/receipt reconciliation, access review and candidate C3 policy proposals; no external actuator/authentication or runtime qualification")

    def __init__(self, profile, evidence, store, world_factory):
        self.profile, self._evidence, self._store = profile, evidence, store
        self._world_factory = world_factory
        self._slot = BoundedSemaphore(1)

    @contextmanager
    def _admit(self):
        if not self._slot.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "C7 operation slot busy", retryable=True)
        try: yield
        finally: self._slot.release()

    def _fingerprint(self, kind, request):
        if request.workspace_id != self.profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C7 workspace differs")
        encoded = canonical(request)
        if len(encoded.encode("utf-8")) > self.profile.max_request_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C7 request byte budget exceeded")
        return sha256((kind + encoded + self.profile.profile_id + IMPLEMENTATION).encode("utf-8")).hexdigest()

    def _operator(self, operator_id):
        if operator_id not in self.profile.operator_ids:
            raise EDIError(ErrorCode.DENIED, "operator ID not configured for this trusted-local profile")

    def _tick(self):
        started = monotonic()
        def tick():
            if monotonic() - started > self.profile.max_operation_seconds:
                raise EDIError(ErrorCode.CAPACITY, "C7 cooperative operation deadline exceeded")
        return tick

    def access_for(self, owner):
        if owner != "C0": raise EDIError(ErrorCode.DENIED, "C7 commands require the C0 workflow lane")
        return AgencyAccess(self)

    def read_policy(self, revision=None):
        value = self._store.policy(revision)
        if value is None: return None
        policy = parsed(PolicyVersion, value)
        verified(Adoption, policy.adoption)
        if policy.adoption.policy is None or policy.adoption.request.decision != "adopt" or policy.adoption.revision != policy.revision:
            raise EDIError(ErrorCode.INTEGRITY, "C7 active policy is not an adopted version")
        return policy

    def get_amendment(self, amendment_id): return verified(Amendment, self._store.get("amendment", amendment_id))
    def get_decision(self, decision_id): return verified(ActionDecision, self._store.get("decision", decision_id))
    def get_actor_view(self, view_id): return verified(ActorView, self._store.get("actor-view", view_id))
    def get_access(self, access_id): return verified(AccessReview, self._store.get("access", access_id))
    def query(self, kind, *, cursor=None, limit=25): return self._store.query(kind, cursor=cursor, limit=limit)

    def request_adoption(self, request: AmendmentRequest):
        with self._admit():
            request = parsed(AmendmentRequest, request)
            fp = self._fingerprint("amendment", request)
            prior = self._store.find("amendment", request.request_id, fp)
            if prior is not None: return verified(Amendment, prior)
            current = self.read_policy()
            head = current.revision if current else 0
            if request.expected_revision != head:
                raise EDIError(ErrorCode.CONFLICT, "C7 amendment base is stale")
            if (head == 0) != (request.change_kind == "bootstrap"):
                raise EDIError(ErrorCode.INVALID, "C7 bootstrap is only valid for an empty policy ledger")
            if current:
                old, new = current.adoption.policy, request.proposed
                changed = (old.purpose, old.purpose_version, old.evaluation_standards) != (new.purpose, new.purpose_version, new.evaluation_standards)
                if changed and (request.change_kind != "goal" or old.purpose_version == new.purpose_version):
                    raise EDIError(ErrorCode.INVALID, "changed purpose/standards require an explicit goal amendment and new purpose version")
                if request.change_kind == "parameter":
                    old_rules = old.model_dump(exclude={"decision_ttl_seconds", "access_cooldown_seconds"})
                    new_rules = new.model_dump(exclude={"decision_ttl_seconds", "access_cooldown_seconds"})
                    if old_rules != new_rules:
                        raise EDIError(ErrorCode.INVALID, "parameter amendment may only change timing parameters")
            result = stamped(Amendment(request=request, created_at=utc_now(), profile_id=self.profile.profile_id, artifact_sha256=""))
            return verified(Amendment, self._store.put("amendment", request.amendment_id, request.request_id, fp, result))

    def decide_adoption(self, request: AdoptionRequest):
        """Trusted local operator API; never exposed on a component/model facade."""
        with self._admit():
            request = parsed(AdoptionRequest, request)
            fp = self._fingerprint("adoption", request)
            self._operator(request.operator_id)
            prior = self._store.find("adoption", request.request_id, fp)
            if prior is not None: return verified(Adoption, prior)
            amendment = self.get_amendment(request.amendment_id)
            if amendment.request.expected_revision != request.expected_revision:
                raise EDIError(ErrorCode.CONFLICT, "amendment/adoption base differs; no implicit rebase")
            revision = request.expected_revision + (1 if request.decision == "adopt" else 0)
            result = stamped(Adoption(request=request, amendment_sha256=amendment.artifact_sha256,
                decided_at=utc_now(), previous_revision=request.expected_revision, revision=revision,
                policy=amendment.request.proposed if request.decision == "adopt" else None, artifact_sha256=""))
            return verified(Adoption, self._store.adopt(result, fp))

    @staticmethod
    def _scope(intent):
        if isinstance(intent, SelectObservations):
            return AccessScope(operation=intent.operation, origin_refs=(intent.origin_ref,), max_items=intent.limit)
        if isinstance(intent, SelectWorld):
            return AccessScope(operation=intent.operation, world_ids=tuple(x.record_id for x in intent.refs), max_items=len(intent.refs))
        return None

    @staticmethod
    def _grants(policy, scope, now):
        return tuple(g for g in policy.grants if g.operation == scope.operation
            and g.not_before <= now < g.expires_at and scope.max_items <= g.max_items
            and set(scope.origin_refs) <= set(g.origin_refs) and set(scope.world_ids) <= set(g.world_ids))

    def check_action(self, request: ActionRequest):
        with self._admit():
            request = parsed(ActionRequest, request)
            fp = self._fingerprint("decision", request)
            prior = self._store.find("decision", request.request_id, fp)
            if prior is not None: return verified(ActionDecision, prior)
            current = self.read_policy()
            if current is None: raise EDIError(ErrorCode.DENIED, "no operational policy is adopted")
            now, policy = utc_now(), current.adoption.policy
            status, reasons = "denied", []
            scope = self._scope(request.intent)
            if request.policy_revision != current.revision: reasons.append("requested policy revision is stale")
            if request.purpose_version != policy.purpose_version: reasons.append("purpose/criteria version differs")
            if scope is None:
                reasons.append("external actions/acquisition and C5 simulation dispatch are not installed in C7; C0 must mediate declared analysis")
            else:
                grants = self._grants(policy, scope, now)
                grant = next((g for g in grants if g.grant_id == request.grant_id), None)
                if grant is None: reasons.append("no named unexpired grant covers the exact operation/scope/items")
                if isinstance(request.intent, SelectObservations) and request.intent.cursor is not None:
                    cursor = request.intent.cursor
                    if cursor.workspace_id != request.workspace_id or cursor.origin_ref != request.intent.origin_ref:
                        reasons.append("C1 cursor must be bound to this workspace and exact granted origin")
                if not reasons:
                    status = "allowed"
                    reasons.append("permitted internal read under the pinned policy and named grant; no external action")
            expiry = now + timedelta(seconds=policy.decision_ttl_seconds)
            if scope is not None:
                matching = next((g for g in self._grants(policy, scope, now) if g.grant_id == request.grant_id), None)
                if matching is not None: expiry = min(expiry, matching.expires_at)
            result = stamped(ActionDecision(request=request, created_at=now, expires_at=expiry,
                policy_adoption_sha256=current.adoption.artifact_sha256, status=status, reasons=tuple(reasons), artifact_sha256=""))
            return verified(ActionDecision, self._store.put("decision", request.decision_id, request.request_id, fp, result))

    def get_receipt(self, execution_id):
        intent = verified(ExecutionIntent, self._store.get("execution-intent", execution_id))
        value = self._store.optional("execution-receipt", execution_id)
        receipt = verified(ExecutionReceipt, value) if value is not None else None
        if receipt is not None and receipt.intent_sha256 != intent.artifact_sha256:
            raise EDIError(ErrorCode.INTEGRITY, "C7 receipt/intent hash differs")
        return ExecutionStatus(intent=intent, receipt=receipt, status="resolved" if receipt else "completion-unresolved")

    def dispatch_authorized(self, request: DispatchRequest):
        with self._admit():
            request = parsed(DispatchRequest, request)
            fp = self._fingerprint("execution-intent", request)
            prior = self._store.find("execution-intent", request.request_id, fp)
            if prior is not None:
                intent = verified(ExecutionIntent, prior)
                return self.get_receipt(intent.request.execution_id)
            decision = self.get_decision(request.decision_id)
            current = self.read_policy()
            if decision.status != "allowed" or current is None:
                raise EDIError(ErrorCode.DENIED, "C7 dispatch requires an allowed decision and adopted policy")
            if decision.policy_adoption_sha256 != current.adoption.artifact_sha256:
                raise EDIError(ErrorCode.CONFLICT, "C7 decision belongs to a superseded policy")
            now = utc_now()
            scope = self._scope(decision.request.intent)
            if scope is None or not any(g.grant_id == decision.request.grant_id for g in self._grants(current.adoption.policy, scope, now)):
                raise EDIError(ErrorCode.DENIED, "C7 grant no longer permits dispatch")
            intent = stamped(ExecutionIntent(request=request, decision=decision, created_at=now,
                profile_id=self.profile.profile_id, artifact_sha256=""))
            raw, started = self._store.begin_execution(intent, fp, now)
            intent = verified(ExecutionIntent, raw)
            if not started: return self.get_receipt(intent.request.execution_id)
            deadline_tick = self._tick()
            def tick():
                deadline_tick()
                self._store.assert_execution(request.execution_id, decision.request.policy_revision)
                current_time = utc_now()
                if not decision.created_at <= current_time < decision.expires_at:
                    raise EDIError(ErrorCode.DENIED, "C7 decision/grant expired or clock regressed during command")
            try:
                command = decision.request.intent
                tick()
                if isinstance(command, SelectObservations):
                    page = self._evidence.replay(cursor=command.cursor, origin_ref=command.origin_ref, limit=command.limit)
                    if page.cursor.workspace_id != request.workspace_id or page.cursor.origin_ref != command.origin_ref:
                        raise EDIError(ErrorCode.INTEGRITY, "C1 returned a different scope")
                    if any(x.scope_id != request.workspace_id or x.origin_ref != command.origin_ref for x in page.items):
                        raise EDIError(ErrorCode.INTEGRITY, "C1 returned an out-of-scope occurrence")
                    result = {"operation": command.operation, "page": page.model_dump(mode="json"), "meaning": "native occurrence metadata; no payload decoding or actor-perception inference"}
                elif isinstance(command, SelectWorld):
                    world, records, size = self._world_factory(), [], 0
                    for ref in command.refs:
                        tick()
                        row = self._model_record(world, ref, command.model_revision)
                        dumped = row.model_dump(mode="json")
                        size += len(canonical(dumped).encode("utf-8"))
                        if size > self.profile.max_result_bytes:
                            raise EDIError(ErrorCode.CAPACITY, "C7 selected model result byte budget exceeded")
                        records.append(dumped)
                    result = {"operation": command.operation, "model_revision": command.model_revision, "records": records,
                        "meaning": "trusted EDI model read; not an actor view or dependency/empirical validity certificate"}
                else:
                    raise EDIError(ErrorCode.UNSUPPORTED, "no external actuator or C5 dispatch adapter is installed")
                tick()
                if len(canonical(result).encode("utf-8")) > self.profile.max_result_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C7 internal result byte budget exceeded")
                receipt = stamped(ExecutionReceipt(execution_id=request.execution_id, intent_sha256=intent.artifact_sha256,
                    finished_at=utc_now(), status="completed", result=result, artifact_sha256=""))
            except EDIError as exc:
                receipt = stamped(ExecutionReceipt(execution_id=request.execution_id, intent_sha256=intent.artifact_sha256,
                    finished_at=utc_now(), status="failed", diagnostic=canonical(exc.as_dict())[:4096], artifact_sha256=""))
            # Unexpected faults/commit errors leave the prepaid intent unresolved; no automatic redispatch.
            self._store.finish_execution(receipt, request.request_id, fp)
            return self.get_receipt(request.execution_id)

    def _model_record(self, world, ref, revision):
        row = world.get(ref.record_id, revision=revision)
        if row.workspace_id != self.profile.workspace_id or row.representation.record_id != ref.record_id:
            raise EDIError(ErrorCode.DENIED, "C7 model correspondence/workspace differs")
        if row.version != ref.version or row.state in ("retired", "rejected", "withdrawn"):
            raise EDIError(ErrorCode.CONFLICT, "C7 selected model version differs or is inactive")
        return row

    def qualify_actor_view(self, request: ActorViewRequest):
        with self._admit():
            request = parsed(ActorViewRequest, request)
            fp = self._fingerprint("actor-view", request)
            prior = self._store.find("actor-view", request.request_id, fp)
            if prior is not None: return verified(ActorView, prior)
            world, tick = self._world_factory(), self._tick()
            actor = self._model_record(world, request.actor, request.model_revision)
            if actor.workspace_id != request.workspace_id or actor.known_at > request.as_of or request.as_of > utc_now():
                raise EDIError(ErrorCode.DENIED, "actor model/workspace/knowledge cut is incompatible")
            for item in request.data:
                tick()
                if item.evidence is not None:
                    ref = item.evidence
                    row = self._evidence.get_record(ref.record_id)
                    if ref.workspace_id != request.workspace_id or row.scope_id != request.workspace_id or row.record_id != ref.record_id:
                        raise EDIError(ErrorCode.DENIED, "actor evidence workspace differs")
                    if row.manifest.sha256 != ref.sha256 or row.capture.origin_class != ref.origin_class or row.capture.lineage != ref.lineage:
                        raise EDIError(ErrorCode.INTEGRITY, "actor evidence digest/origin/lineage differs")
                    if max(row.receipt_time, row.committed_at) > item.available_at:
                        raise EDIError(ErrorCode.DENIED, "actor datum precedes source knowledge cut")
                else:
                    row = self._model_record(world, item.model_ref, request.model_revision)
                    if row.workspace_id != request.workspace_id or row.known_at > item.available_at:
                        raise EDIError(ErrorCode.DENIED, "actor datum precedes model knowledge cut")
            limitations = ("Contents, channels, receipt, attention, memory, frames and goals are attributed inputs, not inferred or independently verified human psychology.",
                "Only explicitly supplied content is exposed. No complete C3 record, hidden global state, automatic traversal or inferred transitive knowledge is appended.",
                "UTC source/model knowledge and actor times share the caller-declared clock mapping. Selector-content correspondence and physical perception remain unestablished.",
                "Available, received and perceived are distinct; C5 actor-response simulation integration is not installed. Evidence/model eligibility does not establish causal truth.")
            result = stamped(ActorView(request=request, created_at=utc_now(), limitations=limitations, artifact_sha256=""))
            return verified(ActorView, self._store.put("actor-view", request.view_id, request.request_id, fp, result))

    @staticmethod
    def _scope_key(request):
        scope = request.scope.model_dump(mode="json")
        scope["origin_refs"], scope["world_ids"] = sorted(scope["origin_refs"]), sorted(scope["world_ids"])
        body = {"scope": scope, "target": request.target, "unknown": request.unknown,
                "hypothesis_family": request.hypothesis_family, "minimum_useful_evidence": request.minimum_useful_evidence}
        return sha256(canonical(body).encode("utf-8")).hexdigest()

    def review_access_scope(self, request: AccessRequest):
        with self._admit():
            request = parsed(AccessRequest, request)
            fp = self._fingerprint("access", request)
            prior = self._store.find("access", request.request_id, fp)
            if prior is not None: return verified(AccessReview, prior)
            now, current, key = utc_now(), self.read_policy(), self._scope_key(request)
            grants = self._grants(current.adoption.policy, request.scope, now) if current else ()
            cooldown = current.adoption.policy.access_cooldown_seconds if current else 604800
            status, related, after = "needs-access", None, now + timedelta(seconds=cooldown)
            disposition = self._store.latest_scope("access-disposition", key)
            previous = self._store.latest_scope("access", key)
            if grants:
                status, after = "existing-grant", min(g.expires_at for g in grants)
            elif disposition is not None:
                value = verified(AccessDisposition, disposition)
                if value.request.until > now:
                    status = "denied-cooldown" if value.request.outcome == "deny" else "deferred"
                    related, after = value.request.disposition_id, value.request.until
            if status == "needs-access" and previous is not None:
                value = verified(AccessReview, previous)
                if value.review_after > now and value.status != "existing-grant":
                    status, related, after = "coalesced", value.related_id or value.request.access_id, value.review_after
            result = stamped(AccessReview(request=request, created_at=now, policy_revision=current.revision if current else 0,
                scope_key=key, status=status, grant_ids=tuple(g.grant_id for g in grants), related_id=related,
                review_after=after, artifact_sha256=""))
            return verified(AccessReview, self._store.put("access", request.access_id, request.request_id, fp, result, scope_key=key))

    def record_access_disposition(self, request: AccessDispositionRequest):
        with self._admit():
            request = parsed(AccessDispositionRequest, request)
            fp = self._fingerprint("access-disposition", request)
            self._operator(request.operator_id)
            prior = self._store.find("access-disposition", request.request_id, fp)
            if prior is not None: return verified(AccessDisposition, prior)
            access = self.get_access(request.access_id)
            if request.until <= utc_now(): raise EDIError(ErrorCode.INVALID, "access denial/defer interval already expired")
            result = stamped(AccessDisposition(request=request, scope_key=access.scope_key, created_at=utc_now(), artifact_sha256=""))
            return verified(AccessDisposition, self._store.put("access-disposition", request.disposition_id, request.request_id, fp, result, scope_key=access.scope_key))

    def archive_report(self, request: ReportRequest):
        with self._admit():
            request = parsed(ReportRequest, request)
            fp = self._fingerprint("report-archive", request)
            prior = self._store.find("report-archive", request.request_id, fp)
            if prior is not None: return verified(ReportArchive, prior)
            self.get_receipt(request.execution_id)
            origin = self._evidence.get_origin(request.origin_ref)
            spec = origin.spec
            if origin.workspace_id != request.workspace_id or spec.namespace != "edi.agency.reports" or spec.adapter != "edi-c7-report/1.0" or spec.deliverer != "C0-local-operator" or spec.binding_basis != "configured":
                raise EDIError(ErrorCode.DENIED, "C7 report requires a dedicated C0-configured report origin")
            stage_fp = self._fingerprint("report-stage", request)
            stage = self._store.find("report-stage", request.request_id, stage_fp)
            payload = request.report_text.encode("utf-8")
            if stage is None:
                now = utc_now()
                capture = Capture(origin_ref=request.origin_ref, idempotency_key="c7-report:" + sha256(request.archive_id.encode()).hexdigest(),
                    kind="execution-report", media_type="text/plain; charset=utf-8", origin_class="generated",
                    lineage=(IMPLEMENTATION, "execution:" + request.execution_id, "local-operator-report"), completeness="complete",
                    expected_bytes=len(payload), expected_sha256=sha256(payload).hexdigest(),
                    time=TemporalScope(reported_time=TimeValue(status="known", value=request.reported_at, reason=None), clock_id="UTC"),
                    profiles={"edi.agency.report": {"execution_id": request.execution_id, "archive_id": request.archive_id,
                        "attribution": request.attribution, "basis": "local-operator-report-not-independent-effect"}})
                stage = self._store.put("report-stage", request.archive_id, request.request_id, stage_fp,
                    ReportStage(request=request, created_at=now, capture=capture))
            stage = parsed(ReportStage, stage)
            receipt = self._evidence.ingest_report(stage.capture, BytesIO(payload))
            row = receipt.observation
            if row.scope_id != request.workspace_id or row.origin_ref != request.origin_ref or row.manifest.sha256 != stage.capture.expected_sha256 or row.capture.origin_class != "generated" or row.capture.lineage != stage.capture.lineage:
                raise EDIError(ErrorCode.INTEGRITY, "C1 archived report receipt differs")
            result = stamped(ReportArchive(stage=stage, receipt=receipt, artifact_sha256=""))
            return verified(ReportArchive, self._store.put("report-archive", request.archive_id, request.request_id, fp, result))

    def reconcile_execution(self, request: ReconcileRequest):
        with self._admit():
            request = parsed(ReconcileRequest, request)
            fp = self._fingerprint("reconciliation", request)
            self._operator(request.operator_id)
            prior = self._store.find("execution-receipt", request.request_id, fp)
            if prior is not None: return verified(ExecutionReceipt, prior)
            status = self.get_receipt(request.execution_id)
            if status.receipt is not None:
                raise EDIError(ErrorCode.CONFLICT, "C7 execution already has an immutable terminal receipt")
            archive = verified(ReportArchive, self._store.get("report-archive", request.archive_id))
            if archive.stage.request.execution_id != request.execution_id:
                raise EDIError(ErrorCode.DENIED, "reconciliation report belongs to a different command")
            result = stamped(ExecutionReceipt(execution_id=request.execution_id, intent_sha256=status.intent.artifact_sha256,
                finished_at=utc_now(), status=request.outcome, report_archive_id=request.archive_id,
                diagnostic=request.rationale[:4096], reconciliation=request.model_dump(mode="json"), artifact_sha256=""))
            return verified(ExecutionReceipt, self._store.finish_execution(result, request.request_id, fp))

    def build_model_patch(self, request: ModelUpdateRequest):
        request = parsed(ModelUpdateRequest, request)
        self._fingerprint("model-stage", request)
        operations = []
        for put in request.operations:
            value = put.representation
            if "edi_c7" in value.properties:
                raise EDIError(ErrorCode.INVALID, "edi_c7 metadata is reserved")
            metadata = {"boundary": request.boundary, "basis": request.basis,
                "attribution": request.attribution[:1024], "source": IMPLEMENTATION,
                "meaning": "candidate represented policy/structure; no operational policy adoption or actual-world effect"}
            operations.append(Put(expected_version=put.expected_version, representation=value.model_copy(update={
                "properties": dict(value.properties, edi_c7=metadata), "method_lineage": value.method_lineage + (IMPLEMENTATION,)})))
        return WorldPatch(workspace_id=request.workspace_id, request_id=request.request_id, base_revision=request.base_revision,
            proposer="C7", reason=request.rationale, change_kind=request.change_kind, operations=tuple(operations))

    def submit_model_update(self, request: ModelUpdateRequest):
        with self._admit():
            request = parsed(ModelUpdateRequest, request)
            fp = self._fingerprint("model-receipt", request)
            prior = self._store.find("model-receipt", request.request_id, fp)
            if prior is not None: return parsed(ModelSubmission, prior)
            stage_fp = self._fingerprint("model-stage", request)
            stage = self._store.find("model-stage", request.request_id, stage_fp)
            if stage is None:
                stage = self._store.put("model-stage", request.request_id, request.request_id, stage_fp,
                    ModelStage(request=request, patch=self.build_model_patch(request)))
            stage = parsed(ModelStage, stage)
            commit = self._world_factory().propose_patch(stage.patch)
            result = ModelSubmission(request=request, commit=commit)
            return parsed(ModelSubmission, self._store.put("model-receipt", request.request_id, request.request_id, fp, result))
