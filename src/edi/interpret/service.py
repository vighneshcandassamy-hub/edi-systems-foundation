from contextlib import contextmanager
from hashlib import sha256
import csv
import platform
import sqlite3
from threading import BoundedSemaphore
from time import monotonic
import pydantic

from edi.interpret.config import InterpretationProfile
from edi.interpret.contracts import (
    Artifact, CheckedClaim, Derivation, DerivationReceipt, InterpretRequest,
    NativeAssociation, SubmissionRequest, Usage,
)
from edi.interpret.decoders import IMPLEMENTATION, decode, select_decoder
from edi.interpret.ports import DerivationStore
from edi.interpret.sqlite import canonical
from edi.interpret.units import check_quantity
from edi.observe.ports import EvidenceReader
from edi.shared.contracts import Capability, EvidenceRef, utc_now
from edi.shared.errors import EDIError, ErrorCode
from edi.world.contracts import HistoryTrajectory, InformationLink, Participant, Put, Ref, Representation, WorldPatch


class Interpretation:
    capability = Capability(
        owner="C2", functions=("F20", "F21", "F22", "F23"), state="implemented-unqualified",
        details="Partial C2: bounded native decoders/features, attributed annotations and association candidates, immutable derivations and candidate-only C3 submission",
    )

    def __init__(self, profile: InterpretationProfile, evidence: EvidenceReader,
                 store: DerivationStore, world_factory):
        self.profile, self._evidence, self._store = profile, evidence, store
        self._world_factory = world_factory
        self._slots = BoundedSemaphore(profile.max_concurrent_operations)

    @contextmanager
    def _admit(self):
        if not self._slots.acquire(blocking=False):
            raise EDIError(ErrorCode.CAPACITY, "C2 operation slots exhausted", retryable=True)
        try:
            yield
        finally:
            self._slots.release()

    def interpret(self, request: InterpretRequest) -> DerivationReceipt:
        try:
            encoded = canonical(request)
            request_bytes = encoded.encode("utf-8", errors="strict")
        except (ValueError, UnicodeError) as exc:
            raise EDIError(ErrorCode.INVALID, "C2 request is not finite UTF-8 JSON") from exc
        if len(request_bytes) > self.profile.max_request_bytes:
            raise EDIError(ErrorCode.CAPACITY, "C2 request limit exceeded")
        request = InterpretRequest.model_validate_json(encoded)
        if request.workspace_id != self.profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "C2 request workspace mismatch")
        versions = {"code": "0.4.0", "python": platform.python_version(),
                    "pydantic": pydantic.__version__, "sqlite": sqlite3.sqlite_version,
                    "csv_field_limit": csv.field_size_limit()}
        fingerprint = sha256((encoded + canonical(self.profile) + IMPLEMENTATION +
                              canonical(versions)).encode("utf-8")).hexdigest()
        with self._admit():
            previous = self._store.find(request.request_id, fingerprint)
            if previous is not None:
                return DerivationReceipt(derivation=previous, duplicate=True)
            started, byte_count = monotonic(), 0
            artifacts, claims, associations, raw = [], [], [], {}
            error = None

            def tick():
                if monotonic() - started > self.profile.max_operation_seconds:
                    raise EDIError(ErrorCode.CAPACITY, "C2 cooperative operation deadline exceeded")

            try:
                for index, spec in enumerate(request.inputs):
                    tick()
                    source = self._evidence.get_record(spec.record_id)
                    if source.scope_id != request.workspace_id:
                        raise EDIError(ErrorCode.DENIED, "C1 returned a different workspace")
                    if source.record_id != spec.record_id:
                        raise EDIError(ErrorCode.INTEGRITY, "C1 returned a different occurrence identity")
                    total = source.manifest.byte_count
                    length = total - spec.offset if spec.length is None else spec.length
                    if spec.offset > total or spec.offset + length > total:
                        raise EDIError(ErrorCode.INVALID, "selected range exceeds C1 payload")
                    selector = "whole-object" if spec.offset == 0 and length == total else f"bytes:{spec.offset}:{spec.offset+length}"
                    evidence = EvidenceRef(workspace_id=request.workspace_id, record_id=source.record_id,
                                           sha256=source.manifest.sha256, selector=selector,
                                           origin_class=source.capture.origin_class, lineage=source.capture.lineage)
                    decoder = select_decoder(spec.decoder, source.manifest.media_type)
                    data, warnings, features = b"", [], {}
                    status, output, failure, selected_hash, verified = "opaque", None, None, None, False
                    try:
                        if decoder != "opaque":
                            unknown = set(source.capture.critical_profiles) - {"native-layout/v1", "coverage/v1"}
                            if unknown:
                                raise EDIError(ErrorCode.UNSUPPORTED, "unknown critical profiles prevent decoding")
                            layout = source.profiles.get("native-layout/v1", {})
                            if isinstance(layout, dict) and decoder in ("text-utf8", "json", "csv"):
                                if layout.get("encoding", "utf-8") not in ("utf-8", "UTF-8"):
                                    raise EDIError(ErrorCode.UNSUPPORTED, "only explicit UTF-8 text decoding is installed")
                                if decoder == "csv" and layout.get("delimiter", spec.delimiter) != spec.delimiter:
                                    raise EDIError(ErrorCode.CONFLICT, "CSV delimiter differs from supplied native-layout profile")
                            if byte_count + length > self.profile.max_input_bytes:
                                raise EDIError(ErrorCode.CAPACITY, "C2 aggregate selected-input byte budget exceeded")
                            parts, offset = [], spec.offset
                            while offset < spec.offset + length:
                                tick()
                                size = min(self.profile.read_chunk_bytes, spec.offset+length-offset)
                                part = self._evidence.read_payload(source.record_id, offset=offset, length=size)
                                if len(part) != size:
                                    raise EDIError(ErrorCode.INCOMPLETE, "C1 range read returned incomplete bytes")
                                parts.append(part)
                                offset += size
                                byte_count += size
                            data = b"".join(parts)
                            selected_hash = sha256(data).hexdigest()
                            if selector == "whole-object":
                                if selected_hash != source.manifest.sha256:
                                    raise EDIError(ErrorCode.INTEGRITY, "C2 aggregate hash differs from C1 manifest")
                                verified = True
                            raw[index] = (spec.offset, data)
                            status, output, features, decoder_warnings = decode(decoder, data, spec.delimiter, self.profile, tick)
                            warnings.extend(decoder_warnings)
                        else:
                            warnings.append("Native reference only; decoder unavailable or opaque explicitly requested")
                        if source.capture.completeness != "complete":
                            warnings.append("Source acquisition completeness is " + source.capture.completeness)
                        if not request.derive_native_features:
                            features = {}
                    except EDIError as exc:
                        status = "unsupported" if exc.code in (ErrorCode.UNSUPPORTED, ErrorCode.CAPACITY) else "failed"
                        failure = exc.as_dict()
                        output, features = None, {}
                    except (ValueError, UnicodeError, EOFError) as exc:
                        status, failure = "failed", {"code": "decode-failed", "message": str(exc)[:512], "retryable": False}
                        output, features = None, {}
                    # csv.Error/wave.Error are normalized inside the decoder facade.
                    artifacts.append(Artifact(
                        input_index=index, evidence=evidence, source_id=source.source_id,
                        origin_ref=source.origin_ref, source_position=source.commit_position,
                        source_time={"capture": source.capture.time.model_dump(mode="json"),
                                     "receipt_time": source.receipt_time.isoformat(),
                                     "committed_at": source.committed_at.isoformat()},
                        decoder_id=decoder, decoder_version=IMPLEMENTATION + ";python=" + platform.python_version(),
                        status=status, selected_offset=spec.offset, selected_length=length,
                        selected_sha256=selected_hash, aggregate_hash_verified=verified, output=output,
                        native_features={"namespace": "edi.native-features/1.0", **features} if request.derive_native_features else {},
                        warnings=tuple(warnings), error=failure,
                    ))
                    if len(canonical([a.model_dump(mode="json") for a in artifacts]).encode("utf-8")) > self.profile.max_output_bytes // 2:
                        raise EDIError(ErrorCode.CAPACITY, "C2 decoded-artifact output budget exceeded")
                for annotation in request.annotations:
                    tick()
                    artifact = artifacts[annotation.input_index]
                    if artifact.status not in ("decoded", "metadata-only"):
                        raise EDIError(ErrorCode.UNSUPPORTED, "annotation input is not decoded/metadata-ready")
                    quote_status = "not-supplied"
                    if annotation.quote_start is not None:
                        start, data = raw[annotation.input_index]
                        a, b = annotation.quote_start-start, annotation.quote_end-start
                        if not 0 <= a <= b <= len(data) or data[a:b] != annotation.quote_utf8.encode("utf-8"):
                            raise EDIError(ErrorCode.INTEGRITY, "annotation quote does not match selected original bytes")
                        quote_status = "verified-byte-match"
                    claims.append(CheckedClaim(annotation=annotation, evidence=artifact.evidence,
                                               quote_status=quote_status,
                                               unit_check=check_quantity(annotation.quantity, annotation.expected_unit)))
                if request.compare_source_and_payload:
                    for left in range(len(artifacts)):
                        for right in range(left+1, len(artifacts)):
                            a, b = artifacts[left], artifacts[right]
                            for relation, matches, rationale in (
                                ("same_source", a.source_id == b.source_id,
                                 "Matching registered C1 source handle; not proof of physical continuity"),
                                ("same_payload", a.evidence.sha256 == b.evidence.sha256,
                                 "Matching whole-payload C1 manifest hashes; not a merged occurrence/entity"),
                            ):
                                if matches:
                                    if len(associations) >= self.profile.max_native_associations:
                                        raise EDIError(ErrorCode.CAPACITY, "native association candidate budget exceeded")
                                    associations.append(NativeAssociation(relation=relation, input_indices=(left, right), rationale=rationale))
            except EDIError as exc:
                error = exc.as_dict()
            status = "complete" if error is None and all(a.status in ("decoded", "metadata-only") for a in artifacts) else "partial"
            if not artifacts or all(a.status in ("unsupported", "failed") for a in artifacts):
                status = "failed"
            content = {"artifacts": [a.model_dump(mode="json") for a in artifacts],
                       "claims": [a.model_dump(mode="json") for a in claims],
                       "native_associations": [a.model_dump(mode="json") for a in associations]}
            content_bytes = canonical(content).encode("utf-8")
            if len(content_bytes) > self.profile.max_output_bytes // 2:
                # Never silently truncate a supposedly complete derivation.
                artifacts, claims, associations = [], [], []
                content_bytes = canonical({"artifacts": [], "claims": [], "native_associations": []}).encode("utf-8")
                status, error = "failed", EDIError(ErrorCode.CAPACITY, "C2 output limit reached; source remains in C1").as_dict()
            derivation = Derivation(
                workspace_id=request.workspace_id,
                derivation_id="d2-" + sha256((request.workspace_id+"\n"+request.request_id+fingerprint).encode("utf-8")).hexdigest(),
                request=request, created_at=utc_now(), status=status,
                profile_snapshot=self.profile.model_dump(mode="json"), runtime_versions=versions,
                artifacts=tuple(artifacts), claims=tuple(claims), native_associations=tuple(associations),
                output_sha256=sha256(content_bytes).hexdigest(),
                usage=Usage(input_bytes_read=byte_count, output_json_bytes=len(content_bytes),
                            elapsed_seconds=monotonic()-started), error=error,
            )
            return self._store.commit(fingerprint, derivation)

    def get_derivation(self, derivation_id):
        with self._admit():
            return self._store.get(derivation_id)

    def _patch(self, request: SubmissionRequest):
        derived = self._store.get(request.derivation_id)
        if derived.status == "failed" or derived.error is not None:
            raise EDIError(ErrorCode.INVALID, "failed/incomplete operation cannot be submitted; inspect derivation")
        operations, ids = [], {}
        for artifact in derived.artifacts:
            record_id = derived.derivation_id + f".source{artifact.input_index}"
            ids[artifact.input_index] = record_id
            operations.append(Put(expected_version=0, representation=Representation(
                record_id=record_id, scope_id=derived.request.scope_id,
                structure=HistoryTrajectory(origin="simulation" if artifact.evidence.origin_class == "simulation" else "source-report"), basis="derivation",
                support=(artifact.evidence,),
                properties={"derivation_id": derived.derivation_id, "artifact_sha256": derived.output_sha256,
                            "decoder": artifact.decoder_id, "decoder_version": artifact.decoder_version,
                            "decode_status": artifact.status, "source_time": artifact.source_time,
                            "source_id": artifact.source_id, "origin_ref": artifact.origin_ref,
                            "descriptive_roles": ["unclassified"], "native_features": artifact.native_features,
                            "warnings": list(artifact.warnings), "error": artifact.error,
                            "derived_artifact_owner": "C2", "independent_new_observation": False},
                method_lineage=(derived.implementation_id, artifact.decoder_version, derived.derivation_id),
            )))
        for index, claim in enumerate(derived.claims):
            if claim.unit_check.get("status") in ("incompatible", "invalid-number"):
                raise EDIError(ErrorCode.INVALID, "invalid/incompatible cardinal quantity annotation blocks submission")
            a = claim.annotation
            properties = a.model_dump(mode="json") | {"quote_status": claim.quote_status, "unit_check": claim.unit_check,
                                                        "derivation_id": derived.derivation_id, "independent_new_observation": False}
            operations.append(Put(expected_version=0, representation=Representation(
                record_id=derived.derivation_id+f".claim{index}", scope_id=derived.request.scope_id,
                structure=HistoryTrajectory(referents=a.referents, origin="source-report"),
                basis="imported" if a.method == "imported-assistance" else "assumption" if a.basis == "assumed" else "derivation",
                support=(claim.evidence,), assumptions=(a.basis_rationale,) if a.basis == "assumed" else (),
                properties=properties, method_lineage=(derived.implementation_id, a.method, *a.assistance_lineage),
            )))
        for index, association in enumerate(derived.native_associations):
            participants = tuple(Participant(ref=Ref(record_id=ids[i]), role="source-report", direction="symmetric") for i in association.input_indices)
            evidence = tuple(derived.artifacts[i].evidence for i in association.input_indices)
            operations.append(Put(expected_version=0, representation=Representation(
                record_id=derived.derivation_id+f".native-link{index}", scope_id=derived.request.scope_id,
                structure=InformationLink(participants=participants), basis="derivation", support=evidence,
                properties=association.model_dump(mode="json"), method_lineage=(derived.implementation_id, "registered-source/hash-comparison"),
            )))
        for index, a in enumerate(derived.request.associations):
            evidence = tuple(derived.artifacts[i].evidence for i in a.input_indices)
            operations.append(Put(expected_version=0, representation=Representation(
                record_id=derived.derivation_id+f".association{index}", scope_id=derived.request.scope_id,
                structure=InformationLink(participants=tuple(Participant(ref=ref, role="proposed-referent") for ref in a.participants)),
                basis="imported" if a.method == "imported-assistance" else "hypothesis", support=evidence,
                properties=a.model_dump(mode="json"), method_lineage=(derived.implementation_id, a.method, *a.assistance_lineage),
            )))
        if len(operations) > 64:
            raise EDIError(ErrorCode.CAPACITY, "C2 candidate batch exceeds initial C3 operation profile; select a smaller derivation")
        return WorldPatch(workspace_id=derived.workspace_id, request_id=request.world_request_id,
                          base_revision=request.base_revision, proposer="C2",
                          reason="Retain attributed C2 derivations/annotations as candidates; no truth or identity promotion",
                          change_kind="explanation", operations=tuple(operations), consumed=request.consumed)

    def build_patch(self, request: SubmissionRequest):
        with self._admit():
            return self._patch(request)

    def submit(self, request: SubmissionRequest):
        with self._admit():
            fingerprint = sha256(canonical(request).encode("utf-8")).hexdigest()
            previous = self._store.submission(request.world_request_id, fingerprint)
            if previous is not None:
                return previous
            patch = self._store.submission_patch(request.world_request_id, fingerprint)
            if patch is None:
                patch = self._store.prepare_submission(request.world_request_id, fingerprint, self._patch(request))
            result = self._world_factory().propose_patch(patch)
            try:
                self._store.record_submission(request.world_request_id, fingerprint, result)
            except EDIError as exc:
                raise EDIError(ErrorCode.UNKNOWN_COMMIT,
                               f"C3 committed request {request.world_request_id} at revision {result.revision}; C2 receipt unresolved; retry same submission",
                               retryable=True) from exc
            return result
