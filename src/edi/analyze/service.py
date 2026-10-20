"""C5 conditional analysis; C0 schedules, C3 owns world state, C6 seals/scores."""
from contextlib import contextmanager
from datetime import datetime
from hashlib import sha256
import math
import platform
from threading import BoundedSemaphore
from time import monotonic

import pydantic

from edi.analyze.backend import Stopped, WorkBudget, backend_versions, require_backend, solve_variant, validate_scenario
from edi.analyze.compiler import COMPILER, IR_KEY, check_world, compile_program, unsupported
from edi.analyze.contracts import CompiledModel, CompileRequest, Diagnostic, Program, RunControl, RunRecord, RunRequest
from edi.analyze.sqlite import canonical
from edi.shared.contracts import Capability, new_id, utc_now
from edi.shared.errors import EDIError, ErrorCode

IMPLEMENTATION = "edi-c5/0.6.0"


def diagnostic(code, message, severity="error"):
    return Diagnostic(code=code, severity=severity, message=message[:8192] or code)


def hashed(record, field):
    return record.model_copy(update={field: sha256(canonical(record).encode("utf-8")).hexdigest()})


class AnalysisAccess:
    """C6 has immutable artifact reads only; no run, cancel or world mutation authority."""
    def __init__(self, service): self._service = service
    def get_run(self, run_id): return self._service.get_run(run_id)
    def get_compiled(self, compiled_id): return self._service.get_compiled(compiled_id)
    def seal_forecast(self, *args, **kwargs):
        raise EDIError(ErrorCode.UNAVAILABLE, "native C6 forecast registration is not installed")


class Analysis:
    capability = Capability(owner="C5", functions=("F50", "F51", "F52", "F53"),
        state="implemented-unqualified",
        details="Partial C5: restricted dimensional stock-flow IR, pinned C3 compilation, isolated optional SciPy scenarios, finite parameter comparisons, immutable conditional trajectories and fenced run lifecycle; qualification open")

    def __init__(self, profile, evidence, store, world_factory):
        self.profile, self._evidence, self._store = profile, evidence, store
        self._world_factory, self._slot = world_factory, BoundedSemaphore(1)

    @contextmanager
    def _admit(self):
        if not self._slot.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "C5 local operation slot busy", retryable=True)
        try: yield
        finally: self._slot.release()

    def _fingerprint(self, operation, request):
        encoded = canonical(request)
        type(request).model_validate_json(encoded)
        if len(encoded.encode("utf-8")) > self.profile.max_request_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C5 request exceeds byte bound")
        if request.workspace_id != self.profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C5 workspace differs")
        semantics = {"workspace_id": self.profile.workspace_id, "profile_id": self.profile.profile_id}
        return sha256((operation + encoded + canonical(semantics) + COMPILER + IMPLEMENTATION).encode("utf-8")).hexdigest()

    def compile(self, request: CompileRequest):
        with self._admit():
            request = CompileRequest.model_validate_json(canonical(request))
            fingerprint = self._fingerprint("compile", request)
            previous = self._store.find_compile(request.request_id, fingerprint)
            if previous is not None: return previous
            port, started = self._world_factory(), monotonic()
            records, views, notes, program, order = {}, [], [], None, ()

            def fetch(ref):
                if monotonic() - started > self.profile.max_operation_seconds:
                    raise EDIError(ErrorCode.CAPACITY, "C5 cooperative compile deadline exceeded")
                if ref.version is None: unsupported("all compilation references require an explicit C3 version")
                if ref.record_id in records:
                    if records[ref.record_id].version != ref.version: unsupported("one compilation cannot mix versions of the same referent")
                    return records[ref.record_id]
                if len(records) >= self.profile.max_world_records:
                    raise EDIError(ErrorCode.CAPACITY, "C5 world cut item limit exceeded")
                item = port.get(ref.record_id, revision=request.model_revision)
                if item.workspace_id != request.workspace_id or item.representation.record_id != ref.record_id or item.version != ref.version:
                    unsupported("C3 selected scope/identity/version differs from the compilation reference")
                if item.state != "accepted_for_use" and not (item.state == "candidate" and request.use_policy == "candidate-exploration"):
                    unsupported("C3 admission state does not permit this declared analysis-use policy")
                records[ref.record_id] = item
                view = port.dependencies(ref.record_id, revision=request.model_revision, max_depth=self.profile.dependency_depth)
                if view.revision != request.model_revision or view.root_id != ref.record_id:
                    unsupported("C3 dependency view differs from the compilation cut")
                views.append(view)
                if not view.complete or any(x.validity != "current" for x in view.items):
                    unsupported("incomplete, missing, inactive or changed dependencies require a new explicit formalization/cut")
                if len(canonical({"world": [v.model_dump(mode="json") for v in records.values()], "dependencies": [v.model_dump(mode="json") for v in views]}).encode("utf-8")) > self.profile.max_context_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "C5 context byte limit exceeded")
                return item

            try:
                mechanism = fetch(request.mechanism_ref)
                structure = mechanism.representation.structure
                if structure.family != "response-relationship" or structure.execution_status == "unsupported":
                    unsupported("C5 requires a declared response relationship, not an unknown/unsupported qualitative law")
                if IR_KEY not in structure.mechanism: unsupported("response has no supported edi_ir_v1 formalization")
                program = Program.model_validate_json(canonical(structure.mechanism[IR_KEY]))
                order = compile_program(program)
                for spec in (*program.stocks, *program.flows): fetch(spec.world_ref)
                check_world(program, records, mechanism)
                notes.append(diagnostic("grammar-supported", "Typed grammar/unit/incidence checks only; physical adequacy, numerical accuracy and causal truth are unqualified", "info"))
                if request.use_policy == "candidate-exploration":
                    notes.append(diagnostic("exploratory-candidate", "Candidate model exploration is explicitly hypothetical; no operational forecast eligibility", "warning"))
                status = "supported"
            except EDIError as exc:
                if exc.code not in (ErrorCode.UNSUPPORTED, ErrorCode.NOT_FOUND): raise
                notes.append(diagnostic("unsupported-model", str(exc)))
                status = "unsupported"
            except ValueError as exc:
                notes.append(diagnostic("invalid-ir", str(exc)))
                status = "unsupported"
            context = {"revision": request.model_revision, "world": [v.model_dump(mode="json") for v in records.values()],
                       "dependencies": [v.model_dump(mode="json") for v in views]}
            artifact = CompiledModel(compiled_id=new_id(), request=request, created_at=utc_now(), status=status,
                program=program, node_order=order, world=tuple(records.values()), dependencies=tuple(views),
                diagnostics=tuple(notes), context_sha256=sha256(canonical(context).encode("utf-8")).hexdigest(),
                artifact_sha256="", profile_snapshot=self.profile.model_dump(mode="json"))
            return self._store.save_compile(fingerprint, hashed(artifact, "artifact_sha256"))

    def get_compiled(self, compiled_id): return self._store.get_compiled(compiled_id)
    def get_run(self, run_id): return self._store.get_run(run_id)
    def status(self, request_id): return self._store.status(request_id)

    def access_for(self, owner):
        if owner != "C6": raise EDIError(ErrorCode.DENIED, "only the allocated C6 read lane is exposed; C0 uses its typed SDK")
        return AnalysisAccess(self)

    def _evidence_metadata(self, refs):
        result = []
        for ref in refs:
            source = self._evidence.get_record(ref.record_id)
            if (ref.workspace_id != self.profile.workspace_id or source.scope_id != ref.workspace_id
                    or source.record_id != ref.record_id or source.manifest.sha256 != ref.sha256
                    or source.capture.origin_class != ref.origin_class or source.capture.lineage != ref.lineage):
                raise EDIError(ErrorCode.INTEGRITY, "C5 scenario evidence differs from the exact C1 occurrence/provenance")
            if ref.selector != "whole-object":
                import re
                match = re.fullmatch(r"bytes:(\d+):(\d+)", ref.selector)
                if match is None or not 0 <= int(match[1]) <= int(match[2]) <= source.manifest.byte_count:
                    raise EDIError(ErrorCode.INVALID, "C5 evidence range selector invalid")
            result.append({"reference": ref.model_dump(mode="json"), "source_id": source.source_id,
                "origin_ref": source.origin_ref, "time": source.capture.time.model_dump(mode="json"),
                "receipt_time": source.receipt_time.isoformat(), "committed_at": source.committed_at.isoformat(),
                "validation": "metadata identity/hash/selector only; scenario numbers remain caller-declared, not parsed measurements"})
        return tuple(result)

    def _record(self, request, compiled, created, status, trajectories=(), envelope=None, differences=(), notes=(), evidence=(), usage=None):
        result = RunRecord(request=request, compiled=compiled, created_at=created, finished_at=utc_now(), status=status,
            trajectories=tuple(trajectories), scenario_envelope=envelope or {}, finite_differences=tuple(differences),
            diagnostics=tuple(notes), evidence_metadata=evidence,
            runtime_versions={"python": platform.python_version(), "pydantic": pydantic.__version__, **backend_versions()},
            usage=usage or {}, artifact_sha256="", profile_snapshot=self.profile.model_dump(mode="json"))
        return hashed(result, "artifact_sha256")

    def run_scenario(self, request: RunRequest):
        with self._admit():
            request = RunRequest.model_validate_json(canonical(request))
            fingerprint = self._fingerprint("run", request)
            previous = self._store.find_run(request.request_id, fingerprint)
            if previous is not None: return previous
            compiled = self._store.get_compiled(request.compiled_id)
            if compiled.request.workspace_id != request.workspace_id: raise EDIError(ErrorCode.DENIED, "compiled model workspace differs")
            # Reserve conservative compact-JSON space before any numerical work.
            program, scenario = compiled.program, request.scenario
            segments = 2 + sum(len(d.points) for d in scenario.drivers)
            width = len(program.stocks) + len(program.flows) if program else 0
            cells = (len(scenario.output_times) + segments) * (1 + width) * (1 + len(scenario.variations))
            # Count retained range/secant values too, not only raw trajectories.
            if program:
                cells += 2 * len(program.stocks) * (len(scenario.output_times) + segments)
                cells += len(program.stocks) * len(scenario.variations)
            estimate = len(canonical(compiled).encode("utf-8")) + len(canonical(request).encode("utf-8")) + 256 * 1024 + 64 * cells
            if cells > self.profile.max_output_cells or estimate > self.profile.max_result_bytes:
                raise EDIError(ErrorCode.CAPACITY, "C5 scenario output/storage envelope exceeds profile; narrow grid or variants")
            evidence = self._evidence_metadata(scenario.evidence)
            created, attempt = utc_now(), new_id()
            intent = {"request": request.model_dump(mode="json"), "created_at": created.isoformat(),
                      "compiled_id": request.compiled_id, "profile": self.profile.model_dump(mode="json")}
            previous = self._store.prepare_run(request, fingerprint, attempt, intent)
            if previous is not None: return previous
            trajectories, notes, envelope, differences = [], list(compiled.diagnostics), {}, []
            budget = WorkBudget(self.profile, lambda: self._store.cancelled(request.request_id, attempt))
            status = "unsupported"
            try:
                budget.tick(force=True)
                if request.mode == "qualitative":
                    if request.solver is not None: raise EDIError(ErrorCode.INVALID, "qualitative mode does not consume solver options")
                    status = "completed" if compiled.status == "supported" else "unsupported"
                    notes.append(diagnostic("qualitative-scope", "Structural/assumption/unsupported diagnostics only; no automatic causal direction, trap diagnosis or numeric prediction", "info"))
                    envelope = {"kind": "structural-diagnostics-only", "unknowns": "causality, omitted systems and parameter uncertainty remain open"}
                elif compiled.status != "supported" or program is None:
                    notes.append(diagnostic("not-executable", "Unsupported compilation cannot generate a numerical trajectory"))
                elif request.solver is None or scenario.actor_information_masks:
                    notes.append(diagnostic("unsupported-scenario", "Numerical mode requires a solver and cannot simulate actor information/policy semantics in this profile"))
                else:
                    require_backend(request.solver)
                    variants = validate_scenario(program, scenario)
                    for name, parameters in variants:
                        budget.tick(force=True)
                        trajectory = solve_variant(compiled, scenario, request.solver, name, parameters, budget)
                        trajectories.append(trajectory)
                    status = "completed" if all(t.status == "completed" for t in trajectories) else "partial"
                    complete = [t for t in trajectories if t.status == "completed"]
                    if complete:
                        grid = complete[0].times
                        envelope = {"kind": "finite-scenario-range; not confidence interval or posterior", "variants": [t.variant for t in complete],
                            "times": list(grid), "states": {s.symbol: {"minimum": [min(t.states[s.symbol][i] for t in complete) for i in range(len(grid))],
                            "maximum": [max(t.states[s.symbol][i] for t in complete) for i in range(len(grid))]} for s in program.stocks},
                            "omitted_variants": [t.variant for t in trajectories if t.status != "completed"], "unquantified": "structural uncertainty, unvisited scenarios, inputs and dependence"}
                    baseline = next((t for t in complete if t.variant == "baseline"), None)
                    if baseline:
                        for other in complete:
                            changed = [key for key in baseline.parameter_values if other.parameter_values[key] != baseline.parameter_values[key]]
                            if len(changed) != 1: continue
                            key = changed[0]
                            delta = other.parameter_values[key] - baseline.parameter_values[key]
                            if not math.isfinite(delta):
                                notes.append(diagnostic("secant-overflow", "Parameter difference overflowed; sensitivity omitted", "warning"))
                                continue
                            effect = {s.symbol: (other.states[s.symbol][-1] - baseline.states[s.symbol][-1]) / delta for s in program.stocks}
                            if any(not math.isfinite(value) for value in effect.values()):
                                notes.append(diagnostic("secant-overflow", "Finite-difference calculation was nonfinite; sensitivity omitted", "warning"))
                                continue
                            differences.append({"variant": other.variant, "parameter": key, "parameter_delta": delta,
                                "final_state_secants": effect, "meaning": "finite conditional secant in declared output-unit/parameter-unit; not an identified causal derivative"})
                    notes.append(diagnostic("uncertainty-limit", "Finite variants and numerical tolerances do not quantify all epistemic uncertainty or identify the real system", "warning"))
            except Stopped as exc:
                status = "cancelled" if exc.cancelled else "partial"
                notes.append(diagnostic("budget-or-cancellation", str(exc)))
            except EDIError as exc:
                if exc.code not in (ErrorCode.UNAVAILABLE, ErrorCode.UNSUPPORTED, ErrorCode.INVALID): raise
                status = "unsupported"
                notes.append(diagnostic(str(exc.code), str(exc)))
            except (ValueError, ArithmeticError, ImportError) as exc:
                status = "partial" if trajectories else "failed"
                notes.append(diagnostic("analysis-failure", str(exc)))
            if self._store.cancelled(request.request_id, attempt): status = "cancelled"
            usage = {"rhs_evaluations_including_failed": budget.evaluations,
                     "elapsed_seconds": monotonic() - budget.started, "llm_calls": 0, "llm_tokens": 0,
                     "requested_variants": 1 + len(scenario.variations), "retained_trajectories": len(trajectories),
                     "cost_scope": "C5 compute only; no measured CPU/energy/provider or complete C0-C6 path cost"}
            result = self._record(request, compiled, created, status, trajectories, envelope, differences, notes, evidence, usage)
            if len(canonical(result).encode("utf-8")) > self.profile.max_result_bytes:
                result = self._record(request, compiled, created, "failed", notes=(*notes, diagnostic("result-overflow", "Numerical outputs exceeded admitted artifact size; not retained, compute usage retained")), evidence=evidence, usage=usage)
            try:
                return self._store.finish(request.request_id, attempt, result)
            except EDIError as exc:
                current = self._store.status(request.request_id)
                if exc.code != ErrorCode.CONFLICT or current is None or current["attempt"] != attempt or not current["cancel_requested"]:
                    raise
                # A cancellation racing the final commit must not become success.
                result = hashed(result.model_copy(update={"status": "cancelled", "artifact_sha256": ""}), "artifact_sha256")
                return self._store.finish(request.request_id, attempt, result)

    def control_run(self, request: RunControl):
        request = RunControl.model_validate_json(canonical(request))
        if request.action == "cancel" and request.expected_attempt is not None:
            raise EDIError(ErrorCode.INVALID, "expected_attempt belongs only to explicit interrupt/fencing")
        fingerprint = self._fingerprint("control", request)
        replacement = new_id() if request.action == "interrupt" else None
        receipt = self._store.control(request, fingerprint, replacement)
        if request.action == "cancel": return receipt
        intent = self._store.intent(request.run_request_id)
        run_request = RunRequest.model_validate_json(canonical(intent["request"]))
        compiled = self._store.get_compiled(intent["compiled_id"])
        created = datetime.fromisoformat(intent["created_at"])
        result = self._record(run_request, compiled, created, "interrupted", notes=(diagnostic("operator-fenced", request.reason),),
            usage={"worker_usage": "unknown after interrupted intent; no automatic rerun", "termination": "operator declared interruption; fencing prevents stale result commits, not process termination"})
        return self._store.finish(request.run_request_id, receipt["replacement_attempt"], result)
