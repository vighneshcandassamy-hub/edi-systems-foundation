"""C6 immutable expectations, local held-out comparison and attributed advice."""
from contextlib import contextmanager
from datetime import timedelta
from hashlib import sha256
from threading import BoundedSemaphore
from time import monotonic

from edi.assess.contracts import (
    Comparison, CompareRequest, Finding, FindingRequest, ForecastReceipt, ForecastSeal,
    PointAssessment, ReviewRequest, RevisionReview, SealConfirmation, SealedPoint, SealRequest,
    StagedSubmission, SubmissionReceipt, SubmissionRequest, YieldRequest, YieldReview,
)
from edi.assess.scoring import scores, summaries
from edi.assess.selection import ScanStopped, reference, select_outcomes
from edi.assess.sqlite import canonical
from edi.shared.contracts import Capability, utc_now
from edi.shared.errors import EDIError, ErrorCode
from edi.world.contracts import Put, Ref, WorldPatch, iter_refs

IMPLEMENTATION = "edi-c6/0.7.0"
CAUSES = ("observation-error", "semantic-misalignment", "numerical-error", "unexpected-drivers",
          "wrong-parameters", "wrong-rule-or-topology", "changed-policy", "non-identifiability")


def parsed(cls, document): return cls.model_validate_json(canonical(document))


def digest(record):
    return sha256(canonical(record.model_copy(update={"artifact_sha256": ""})).encode("utf-8")).hexdigest()


def stamped(record): return record.model_copy(update={"artifact_sha256": digest(record)})


class AssessmentAccess:
    def __init__(self, service, owner): self._service, self._owner = service, owner
    def query_assessments(self, kind="comparison", *, cursor=None, limit=25):
        if self._owner != "C4": raise EDIError(ErrorCode.DENIED, "C5 has no assessment selection lane")
        return self._service.query(kind, cursor=cursor, limit=limit)
    def review_inquiry_yield(self, request):
        if self._owner != "C4": raise EDIError(ErrorCode.DENIED, "only the C4 inquiry-review lane is allocated")
        return self._service.review_inquiry_yield(request)
    def seal_forecast(self, request):
        if self._owner != "C5": raise EDIError(ErrorCode.DENIED, "C4 cannot register C5 forecast output through this facade")
        return self._service.seal_forecast(request)
    def get_forecast(self, forecast_id):
        if self._owner != "C5": raise EDIError(ErrorCode.DENIED, "C5 forecast receipt lane required")
        return self._service.get_forecast(forecast_id)


class Assessment:
    capability = Capability(owner="C6", functions=("F60", "F61", "F62", "F63"), state="implemented-unqualified",
        details="Partial C6: durable forecast/confirmation, deterministic bounded external-outcome selection, point/Brier scores and descriptive calibration, attributed diagnostic/revision/finding records, candidate-only C3 submission; scientific qualification open")

    def __init__(self, profile, evidence, store, world_factory, analysis_factory):
        self.profile, self._evidence, self._store = profile, evidence, store
        self._world_factory, self._analysis_factory = world_factory, analysis_factory
        self._slot = BoundedSemaphore(1)

    @contextmanager
    def _admit(self):
        if not self._slot.acquire(blocking=False): raise EDIError(ErrorCode.CAPACITY, "C6 operation slot busy", retryable=True)
        try: yield
        finally: self._slot.release()

    def _fingerprint(self, kind, request):
        encoded = canonical(request)
        if len(encoded.encode("utf-8")) > self.profile.max_request_bytes: raise EDIError(ErrorCode.CAPACITY, "C6 request byte limit exceeded")
        if request.workspace_id != self.profile.workspace_id: raise EDIError(ErrorCode.DENIED, "C6 request workspace differs")
        semantics = {"workspace_id": self.profile.workspace_id, "profile_id": self.profile.profile_id}
        return sha256((kind + encoded + canonical(semantics) + IMPLEMENTATION).encode("utf-8")).hexdigest()

    def _deadline(self):
        started = monotonic()
        def tick():
            if monotonic() - started > self.profile.max_operation_seconds:
                raise EDIError(ErrorCode.CAPACITY, "C6 cooperative operation deadline exceeded")
        return tick

    def access_for(self, owner):
        if owner not in ("C4", "C5"): raise EDIError(ErrorCode.DENIED, "no C6 component lane allocated")
        return AssessmentAccess(self, owner)

    def query(self, kind="comparison", *, cursor=None, limit=25): return self._store.query(kind, cursor=cursor, limit=limit)
    def _verified(self, cls, document):
        result = parsed(cls, document)
        if digest(result) != result.artifact_sha256:
            raise EDIError(ErrorCode.INTEGRITY, "C6 stored artifact content digest differs")
        return result

    def get_comparison(self, assessment_id): return self._verified(Comparison, self._store.get("comparison", assessment_id))
    def get_review(self, review_id): return self._verified(RevisionReview, self._store.get("review", review_id))
    def get_finding(self, finding_id): return self._verified(Finding, self._store.get("finding", finding_id))

    def get_forecast(self, forecast_id):
        seal = self._verified(ForecastSeal, self._store.get("forecast", forecast_id))
        document = self._store.optional("confirmation", forecast_id)
        confirmation = self._verified(SealConfirmation, document) if document else None
        return ForecastReceipt(seal=seal, confirmation=confirmation)

    def _confirm(self, seal):
        if digest(seal) != seal.artifact_sha256:
            raise EDIError(ErrorCode.INTEGRITY, "C6 forecast payload digest differs")
        existing = self._store.optional("confirmation", seal.request.forecast_id)
        if existing is None:
            now = utc_now()  # Observed only after the initial forecast payload commit returned.
            lead = float(seal.profile_snapshot["minimum_lead_seconds"])
            status = "local-prospective" if all((p.target_time - now).total_seconds() > lead for p in seal.points) else "late-confirmation"
            item = stamped(SealConfirmation(forecast_id=seal.request.forecast_id, seal_sha256=seal.artifact_sha256,
                acknowledgement_observed_at=now, status=status,
                clock_assumption="Trusted common host UTC and honest source event/report clocks assumed; no external timestamp authority or knowledge-independence proof", artifact_sha256=""))
            existing = self._store.put("confirmation", seal.request.forecast_id, seal.request.forecast_id,
                                       seal.artifact_sha256, item)
        return ForecastReceipt(seal=seal, confirmation=self._verified(SealConfirmation, existing))

    def seal_forecast(self, request: SealRequest):
        with self._admit():
            request = parsed(SealRequest, request)
            fingerprint = self._fingerprint("forecast", request)
            original = self._store.find("forecast", request.request_id, fingerprint)
            if original is not None: return self._confirm(parsed(ForecastSeal, original))
            tick = self._deadline()
            run = self._analysis_factory().get_run(request.run_id)
            if len(canonical(run).encode("utf-8")) > self.profile.max_context_bytes:
                raise EDIError(ErrorCode.CAPACITY, "C6 C5 run context limit exceeded")
            if (run.request.workspace_id != request.workspace_id or run.request.run_id != request.run_id
                    or run.status != "completed" or run.request.mode != "numerical" or run.compiled.status != "supported"
                    or digest(run) != run.artifact_sha256 or digest(run.compiled) != run.compiled.artifact_sha256):
                raise EDIError(ErrorCode.INVALID, "C6 registration requires exact immutable completed C5 numerical output")
            program = run.compiled.program
            origin = run.request.scenario.time_origin
            if program is None or origin.status != "known": raise EDIError(ErrorCode.UNSUPPORTED, "prospective correspondence requires a declared absolute scenario time origin")
            trajectory = next((t for t in run.trajectories if t.variant == request.variant and t.status == "completed"), None)
            if trajectory is None: raise EDIError(ErrorCode.INVALID, "selected C5 variant has no completed trajectory")
            if len({c.case_id for c in request.cases}) != len(request.cases): raise EDIError(ErrorCode.CONFLICT, "forecast case IDs must be distinct")
            refs = {canonical(r): r for r in run.request.scenario.evidence}
            for item in run.compiled.world:
                for ref in item.representation.support + item.representation.counterevidence: refs[canonical(ref)] = ref
            if len(refs) > self.profile.max_input_refs: raise EDIError(ErrorCode.CAPACITY, "forecast input-reference budget exceeded")
            input_sources = set()
            for ref in refs.values():
                tick()
                source = self._evidence.get_record(ref.record_id)
                if (source.scope_id != request.workspace_id or ref.workspace_id != request.workspace_id or source.record_id != ref.record_id
                        or source.manifest.sha256 != ref.sha256 or source.capture.origin_class != ref.origin_class or source.capture.lineage != ref.lineage
                        or source.committed_at > run.created_at):
                    raise EDIError(ErrorCode.INTEGRITY, "forecast input provenance/availability differs from its declared C5 cut")
                input_sources.add(source.source_id)
            stocks = {s.symbol: s for s in program.stocks}
            channels = {c.stock_symbol for c in run.request.scenario.correspondence}
            points, bindings, uniqueness = [], {}, set()
            for case in request.cases:
                tick()
                if case.stock_symbol not in stocks or case.stock_symbol not in channels or case.relative_time not in trajectory.times:
                    raise EDIError(ErrorCode.INVALID, "forecast case must select a C5 stock/output sample with declared correspondence; no interpolation")
                target = origin.value + timedelta(seconds=case.relative_time)
                if (target - utc_now()).total_seconds() <= self.profile.minimum_lead_seconds:
                    raise EDIError(ErrorCode.INVALID, "new forecast target must remain in the future; never backdate registration")
                key = (case.origin_ref, case.variable, target)
                if key in uniqueness: raise EDIError(ErrorCode.CONFLICT, "one observed outcome cannot be duplicated within a forecast denominator")
                uniqueness.add(key)
                value = trajectory.states[case.stock_symbol][trajectory.times.index(case.relative_time)]
                stock = stocks[case.stock_symbol]
                if case.interpretation == "bernoulli-probability" and (stock.unit.symbol != "1" or stock.unit.dimensions or not 0 <= value <= 1 or case.score_limit > 1):
                    raise EDIError(ErrorCode.INVALID, "Brier interpretation needs an explicitly dimensionless probability and limit in [0,1]")
                points.append(SealedPoint(case=case, target_time=target, predicted=value, unit=stock.unit, world_ref=stock.world_ref))
                if case.origin_ref not in bindings:
                    binding = self._evidence.get_origin(case.origin_ref)
                    if binding.workspace_id != request.workspace_id or binding.origin_ref != case.origin_ref:
                        raise EDIError(ErrorCode.INTEGRITY, "forecast outcome origin differs from requested scope")
                    bindings[case.origin_ref] = binding
            if len(bindings) > self.profile.max_origins: raise EDIError(ErrorCode.CAPACITY, "forecast origin budget exceeded")
            coverage = self._evidence.coverage()
            if coverage["workspace_id"] != request.workspace_id: raise EDIError(ErrorCode.INTEGRITY, "C1 registration coverage workspace differs")
            seal = stamped(ForecastSeal(request=request, prepared_at=utc_now(), c1_watermark=coverage["watermark"],
                run_sha256=run.artifact_sha256, compiled_sha256=run.compiled.artifact_sha256,
                model_revision=run.compiled.request.model_revision, run_request=run.request, program_snapshot=program,
                active_parameters=trajectory.parameter_values,
                model_refs=tuple(Ref(record_id=v.representation.record_id, version=v.version) for v in run.compiled.world),
                model_assumptions=program.assumptions + run.request.scenario.assumptions,
                inputs=tuple(refs.values()), input_source_ids=tuple(sorted(input_sources)), outcome_origins=tuple(bindings.values()),
                points=tuple(points), artifact_sha256="", profile_snapshot=self.profile.model_dump(mode="json")))
            tick()
            stored = parsed(ForecastSeal, self._store.put("forecast", request.forecast_id, request.request_id, fingerprint, seal))
            return self._confirm(stored)

    def compare_outcome(self, request: CompareRequest):
        with self._admit():
            request = parsed(CompareRequest, request)
            fingerprint = self._fingerprint("comparison", request)
            original = self._store.find("comparison", request.request_id, fingerprint)
            if original is not None: return parsed(Comparison, original)
            receipt = self.get_forecast(request.forecast_id)
            seal, confirmation = receipt.seal, receipt.confirmation
            if confirmation is None: raise EDIError(ErrorCode.INCOMPLETE, "forecast payload has no durable acknowledgement confirmation")
            coverage = self._evidence.coverage()
            if (coverage["workspace_id"] != request.workspace_id
                    or not seal.c1_watermark <= request.outcome_watermark <= coverage["watermark"]):
                raise EDIError(ErrorCode.INTEGRITY, "C1 outcome coverage differs from the sealed source cut")
            started = monotonic()
            def tick():
                if monotonic() - started > self.profile.max_operation_seconds: raise ScanStopped("cooperative outcome-selection deadline exceeded")
            chosen, blocked, source_coverage, usage = select_outcomes(self._evidence, seal, request.outcome_watermark, self.profile, tick)
            complete = {c["origin_ref"]: c["exhausted"] for c in source_coverage}
            results = []
            for point in seal.points:
                case_id, issues = point.case.case_id, []
                source, measurement = chosen.get(case_id, (None, None))
                status, losses, within = "missing", {}, None
                if case_id in blocked:
                    source, issue = blocked[case_id]
                    measurement = None
                    status = "invalid"; issues.append(issue)
                elif source is None:
                    status = "missing" if complete.get(point.case.origin_ref, False) else "scan-incomplete"
                    issues.append("no matching measurement in the selected prefix; missing never implies zero error or world absence")
                else:
                    at = confirmation.acknowledgement_observed_at
                    reported = source.capture.time.reported_time
                    if (confirmation.status != "local-prospective" or confirmation.seal_sha256 != seal.artifact_sha256
                            or source.commit_position <= seal.c1_watermark or source.receipt_time <= at
                            or source.committed_at <= at or point.target_time <= at):
                        issues.append("outcome is not held out after a confirmed future registration")
                    if (measurement.observed_at != point.target_time or measurement.observed_at != source.capture.time.event_time.value
                            or reported.status != "known" or not point.target_time <= reported.value <= source.receipt_time <= source.committed_at):
                        issues.append("event/report/receipt correspondence or clock order is incompatible")
                    if source.capture.origin_class != "external" or source.capture.lineage:
                        issues.append("strict raw-external outcome profile rejects generated/unknown/derived lineage")
                    if measurement.unit != point.unit.symbol: issues.append("measurement unit differs; no implicit conversion")
                    dependent = source.source_id in seal.input_source_ids
                    if dependent and seal.request.rule.require_disjoint_sources: issues.append("outcome source overlaps declared forecast input sources")
                    if issues: status = "ineligible"
                    elif measurement.status != "observed":
                        status = "missing" if measurement.status == "missing" else "censored"
                        issues.append("missing/censored observation retained without imputation or ordinary scalar score")
                    else:
                        try:
                            losses, within = scores(point, measurement)
                            status = "scored"
                            if dependent: issues.append("shared input/outcome source allowed by sealed policy; dependence remains and no iid claim follows")
                        except (ValueError, ArithmeticError) as exc:
                            status = "invalid"; issues.append(str(exc)[:1024])
                results.append(PointAssessment(point=point, status=status, evidence=reference(source) if source else None,
                    observation=measurement, source_id=source.source_id if source else None,
                    scores=losses, within_declared_limit=within, issues=tuple(issues)))
            usage.update(elapsed_seconds=monotonic() - started, llm_calls=0, llm_tokens=0,
                         cost_scope="C6 local scan/scoring only; energy, full pipeline and failed pre-admission work unmeasured")
            try: summary = summaries(results, seal.request.rule)
            except ArithmeticError:
                summary = {"status": "summary-overflow; individual finite results retained", "planned_count": len(results)}
            result = stamped(Comparison(request=request, created_at=utc_now(), forecast=receipt, outcome_watermark=request.outcome_watermark,
                results=tuple(results), source_coverage=source_coverage, summaries=summary,
                possible_causes={key: "not-established" for key in CAUSES},
                limitations=("Local store/source timestamps and declared raw provenance do not prove global independence or absence of hidden prior knowledge",
                    "Point errors or Brier loss do not identify causal structure, calibrate a model by themselves or establish EDI superiority",
                    "Unknown dependence, source completeness, C5 numerical qualification, selection/exposure and clock trust remain explicit assumptions"),
                usage=usage, artifact_sha256="", profile_snapshot=self.profile.model_dump(mode="json")))
            return parsed(Comparison, self._store.put("comparison", request.assessment_id, request.request_id, fingerprint, result))

    def _allowed_evidence(self, assessment):
        refs = {canonical(ref): ref for ref in assessment.forecast.seal.inputs}
        for row in assessment.results:
            if row.evidence is not None: refs[canonical(row.evidence)] = row.evidence
        return refs

    def _check_refs(self, refs, allowed):
        if any(canonical(ref) not in allowed for ref in refs):
            raise EDIError(ErrorCode.INTEGRITY, "advice/finding cites evidence outside the immutable assessment cut")

    def review_revision(self, request: ReviewRequest):
        with self._admit():
            request = parsed(ReviewRequest, request)
            fingerprint = self._fingerprint("review", request)
            previous = self._store.find("review", request.request_id, fingerprint)
            if previous is not None: return parsed(RevisionReview, previous)
            assessment = self.get_comparison(request.assessment_id)
            allowed = self._allowed_evidence(assessment)
            tick = self._deadline()
            port, targets, views, notes = self._world_factory(), [], [], []
            if len({ref.record_id for ref in request.targets}) != len(request.targets):
                raise EDIError(ErrorCode.CONFLICT, "revision targets must be distinct pinned referents")
            for ref in request.targets:
                tick()
                if ref.version is None: raise EDIError(ErrorCode.INVALID, "revision targets require explicit versions")
                item = port.get(ref.record_id, revision=request.model_revision)
                if item.workspace_id != request.workspace_id or item.version != ref.version or item.representation.record_id != ref.record_id:
                    raise EDIError(ErrorCode.INTEGRITY, "revision target does not match its requested C3 cut")
                if item.state not in ("candidate", "accepted_for_use"):
                    raise EDIError(ErrorCode.DENIED, "C6 cannot implicitly resurrect rejected, withdrawn or retired targets")
                targets.append(item.model_dump(mode="json"))
                if len(canonical(targets).encode("utf-8")) > self.profile.max_context_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C6 revision target-context byte budget exceeded")
                view = port.dependencies(ref.record_id, revision=request.model_revision, direction="dependents", max_depth=2)
                if view.root_id != ref.record_id or view.revision != request.model_revision:
                    raise EDIError(ErrorCode.INTEGRITY, "revision dependency view differs from selected cut")
                views.append(view)
                if not view.complete: notes.append("affected descendants truncated for " + ref.record_id + "; no exhaustive impact claim")
            for cause in request.causes: self._check_refs(cause.support + cause.counterevidence, allowed)
            base = {ref.record_id: ref.version for ref in request.targets}
            changed = set()
            for put in request.candidates:
                value = put.representation
                if put.admission is not None or value.basis != "hypothesis" or value.record_id in changed:
                    raise EDIError(ErrorCode.DENIED, "C6 edits must be distinct candidate hypothesis puts, never admission or retirement")
                changed.add(value.record_id)
                if put.expected_version != base.get(value.record_id, 0):
                    raise EDIError(ErrorCode.INVALID, "candidate edit requires selected target version; new records require zero")
                self._check_refs(value.support + value.counterevidence, allowed)
            for put in request.candidates:
                for ref in iter_refs(put.representation):
                    if ref.record_id in changed and ref.version is None: continue
                    if ref.record_id not in base or ref.version != base[ref.record_id]:
                        raise EDIError(ErrorCode.INVALID, "candidate dependencies must use pinned selected targets or explicit post-patch candidates")
                if "edi_c6" in put.representation.properties:
                    raise EDIError(ErrorCode.INVALID, "edi_c6 is reserved controller attribution")
            notes.append("Causes, recommendation and expected benefit are attributed hypotheses; prediction fit does not identify causal structure")
            result = stamped(RevisionReview(request=request, created_at=utc_now(), assessment_sha256=assessment.artifact_sha256,
                dependent_views=tuple(views), target_snapshot=tuple(targets), limitations=tuple(notes), artifact_sha256=""))
            return parsed(RevisionReview, self._store.put("review", request.review_id, request.request_id, fingerprint, result))

    def draft_finding(self, request: FindingRequest):
        with self._admit():
            request = parsed(FindingRequest, request)
            fingerprint = self._fingerprint("finding", request)
            previous = self._store.find("finding", request.request_id, fingerprint)
            if previous is not None: return parsed(Finding, previous)
            review = self.get_review(request.review_id)
            assessment = self.get_comparison(review.request.assessment_id)
            self._check_refs(request.support + request.counterevidence, self._allowed_evidence(assessment))
            if request.expiry <= utc_now(): raise EDIError(ErrorCode.INVALID, "new finding must have a future expiry")
            result = stamped(Finding(request=request, created_at=utc_now(), review_sha256=review.artifact_sha256, artifact_sha256=""))
            return parsed(Finding, self._store.put("finding", request.finding_id, request.request_id, fingerprint, result))

    def review_inquiry_yield(self, request: YieldRequest):
        with self._admit():
            request = parsed(YieldRequest, request)
            fingerprint = self._fingerprint("yield", request)
            previous = self._store.find("yield", request.request_id, fingerprint)
            if previous is not None: return parsed(YieldReview, previous)
            if len(set(request.assessment_ids)) != len(request.assessment_ids):
                raise EDIError(ErrorCode.CONFLICT, "duplicate assessments cannot inflate inquiry yield")
            seen, scored, planned, sources, hashes, context_bytes = set(), 0, 0, set(), [], 0
            tick = self._deadline()
            for assessment_id in request.assessment_ids:
                tick()
                assessment = self.get_comparison(assessment_id)
                context_bytes += len(canonical(assessment).encode("utf-8"))
                if context_bytes > self.profile.max_context_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C6 inquiry-review context byte budget exceeded")
                hashes.append(assessment.artifact_sha256)
                for row in assessment.results:
                    key = (assessment.forecast.seal.request.forecast_id, row.point.case.case_id)
                    if key in seen: raise EDIError(ErrorCode.CONFLICT, "same forecast case appears in multiple outcome snapshots; select one explicit snapshot")
                    seen.add(key); planned += 1
                    if row.status == "scored": scored += 1; sources.add(row.source_id)
            result = stamped(YieldReview(request=request, created_at=utc_now(),
                assessment_hashes=tuple(hashes),
                coverage={"linked_assessments": len(hashes), "planned_cases": planned, "scored_cases": scored,
                    "unique_sources": len(sources), "declared_exposure": request.declared_exposure,
                    "selection": "caller-declared assessment set; completeness and matched discrimination benefit not established",
                    "cost": "caller-declared account retained; no measured end-to-end efficiency or causal information gain"}, artifact_sha256=""))
            return parsed(YieldReview, self._store.put("yield", request.yield_id, request.request_id, fingerprint, result))

    def build_patch(self, request: SubmissionRequest):
        self._fingerprint("stage", request)
        review = self.get_review(request.review_id)
        if not review.request.candidates: raise EDIError(ErrorCode.INVALID, "revision review has no candidate model changes")
        assessment = self.get_comparison(review.request.assessment_id)
        operations = []
        for put in review.request.candidates:
            value = put.representation
            properties = dict(value.properties)
            properties["edi_c6"] = {"review_id": review.request.review_id, "review_sha256": review.artifact_sha256,
                "assessment_id": assessment.request.assessment_id, "assessment_sha256": assessment.artifact_sha256,
                "recommendation": review.request.recommendation, "attribution_summary": review.request.attribution[:1024],
                "rationale_summary": review.request.rationale[:2048], "retained_rival_count": len(review.request.retained_rivals),
                "cause_categories": list(dict.fromkeys(c.category for c in review.request.causes)),
                "verification_summary": review.request.new_verification_burden[:2048],
                "full_advice": "immutable C6 review ID/hash; metadata summaries may be truncated",
                "validity": "candidate advice; assessment eligibility/uncertainty remains scoped"}
            operations.append(Put(expected_version=put.expected_version,
                representation=value.model_copy(update={"properties": properties,
                    "method_lineage": value.method_lineage + (IMPLEMENTATION, review.artifact_sha256, assessment.artifact_sha256)})))
        return WorldPatch(workspace_id=request.workspace_id, request_id=request.request_id,
            base_revision=review.request.model_revision, proposer="C6", reason=request.reason,
            change_kind="explanation", operations=tuple(operations))

    def submit_revision(self, request: SubmissionRequest):
        with self._admit():
            request = parsed(SubmissionRequest, request)
            fingerprint = self._fingerprint("receipt", request)
            previous = self._store.find("receipt", request.request_id, fingerprint)
            if previous is not None: return parsed(SubmissionReceipt, previous)
            stage_fingerprint = self._fingerprint("stage", request)
            stage = self._store.find("stage", request.request_id, stage_fingerprint)
            if stage is None:
                draft = StagedSubmission(request=request, patch=self.build_patch(request))
                stage = self._store.put("stage", request.request_id, request.request_id, stage_fingerprint, draft)
            stage = parsed(StagedSubmission, stage)
            commit = self._world_factory().propose_patch(stage.patch)
            receipt = SubmissionReceipt(request=request, commit=commit)
            return parsed(SubmissionReceipt, self._store.put("receipt", request.request_id, request.request_id, fingerprint, receipt))
