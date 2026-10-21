"""C2 derivation/annotation records. Neither decoding nor a label confers truth."""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.shared.contracts import EvidenceRef, Identifier, Quantity, Record
from edi.world.contracts import ConsumedEvidence, Ref

Decoder = Literal["auto", "text-utf8", "json", "csv", "png-metadata", "wav-metadata", "opaque"]
Role = Literal["event", "state_sample", "rate_sample", "pattern", "structure", "mechanism", "purpose", "unclassified"]


class InputSpec(Record):
    record_id: Identifier
    decoder: Decoder = "auto"
    offset: int = Field(default=0, ge=0)
    length: int | None = Field(default=None, ge=0)
    delimiter: Annotated[str, Field(min_length=1, max_length=1)] = ","

    @model_validator(mode="after")
    def separator(self):
        if self.delimiter in "\r\n\x00":
            raise ValueError("CSV delimiter cannot be a newline or NUL")
        return self


class AssistanceProvenance(Record):
    producer: Identifier
    model_or_checkpoint: Identifier
    prompt_version: Identifier
    tool_schema_version: Identifier
    configuration: dict[str, JsonValue] = Field(default_factory=dict)


class ClaimAnnotation(Record):
    input_index: int = Field(ge=0)
    statement: Annotated[str, Field(min_length=1, max_length=4096)]
    roles: tuple[Role, ...] = ("unclassified",)
    role_rationale: str = "unclassified; no semantic classifier executed"
    basis: Literal["measured_or_inspected", "reported", "inferred", "assumed", "unknown"] = "unknown"
    basis_rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    referents: tuple[Ref, ...] = ()
    # Absolute source byte offsets, separate from derived CSV/JSON paths.
    quote_start: int | None = Field(default=None, ge=0)
    quote_end: int | None = Field(default=None, ge=0)
    quote_utf8: str | None = None
    quantity: Quantity | None = None
    expected_unit: str | None = None
    meaning: dict[str, JsonValue] = Field(default_factory=dict)
    method: Literal["operator-supplied", "imported-assistance"] = "operator-supplied"
    assistance_lineage: tuple[str, ...] = ()
    assistance: AssistanceProvenance | None = None

    @model_validator(mode="after")
    def attribution(self):
        if not self.roles or not self.role_rationale:
            raise ValueError("descriptive roles require a rationale")
        if self.method == "imported-assistance" and (not self.assistance_lineage or self.assistance is None):
            raise ValueError("imported assistance requires producer/model/prompt lineage")
        quote = (self.quote_start, self.quote_end, self.quote_utf8)
        if any(v is not None for v in quote) and not all(v is not None for v in quote):
            raise ValueError("quote requires both absolute bounds and exact UTF-8 text")
        if self.quote_start is not None and (self.quote_end <= self.quote_start or not self.quote_utf8):
            raise ValueError("a quoted span must be nonempty with increasing bounds")
        return self


class AssociationAnnotation(Record):
    relation: Literal["mentions_same_entity", "possible_same_physical_referent", "part_of", "replacement_of"]
    participants: tuple[Ref, ...] = Field(min_length=2, max_length=8)
    input_indices: tuple[int, ...] = Field(min_length=1)
    rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    alternatives_and_contradictions: tuple[str, ...] = ()
    method: Literal["operator-supplied", "imported-assistance"] = "operator-supplied"
    assistance_lineage: tuple[str, ...] = ()
    assistance: AssistanceProvenance | None = None

    @model_validator(mode="after")
    def lineage(self):
        if self.method == "imported-assistance" and (not self.assistance_lineage or self.assistance is None):
            raise ValueError("imported association requires assistance lineage")
        return self


class InterpretRequest(Record):
    workspace_id: Identifier
    request_id: Identifier
    inputs: tuple[InputSpec, ...] = Field(min_length=1, max_length=8)
    annotations: tuple[ClaimAnnotation, ...] = Field(default=(), max_length=16)
    associations: tuple[AssociationAnnotation, ...] = Field(default=(), max_length=16)
    derive_native_features: bool = True
    compare_source_and_payload: bool = True
    scope_id: Identifier = "world"

    @model_validator(mode="after")
    def indices(self):
        indices = [a.input_index for a in self.annotations]
        indices += [i for a in self.associations for i in a.input_indices]
        if any(i < 0 or i >= len(self.inputs) for i in indices):
            raise ValueError("annotation input index outside request")
        return self


class Artifact(Record):
    input_index: int
    evidence: EvidenceRef
    source_id: str
    origin_ref: str
    source_position: int
    source_time: dict[str, JsonValue]
    decoder_id: str
    decoder_version: str
    status: Literal["decoded", "metadata-only", "opaque", "unsupported", "failed"]
    selected_offset: int
    selected_length: int
    selected_sha256: str | None = None
    aggregate_hash_verified: bool = False
    output: JsonValue = None
    native_features: dict[str, JsonValue] = Field(default_factory=dict)
    warnings: tuple[str, ...] = ()
    error: dict[str, JsonValue] | None = None


class CheckedClaim(Record):
    annotation: ClaimAnnotation
    evidence: EvidenceRef
    quote_status: Literal["verified-byte-match", "not-supplied"]
    unit_check: dict[str, JsonValue]


class NativeAssociation(Record):
    relation: Literal["same_source", "same_payload"]
    input_indices: tuple[int, int]
    rationale: str
    status: Literal["candidate"] = "candidate"


class Usage(Record):
    input_bytes_read: int = Field(ge=0)
    output_json_bytes: int = Field(ge=0)
    elapsed_seconds: float = Field(ge=0)
    model_calls: Literal[0] = 0
    model_tokens: Literal[0] = 0
    scope: Literal["C2 transform before commit; includes C1 reads; excludes acquisition, artifact-commit latency and C3"] = "C2 transform before commit; includes C1 reads; excludes acquisition, artifact-commit latency and C3"


class Derivation(Record):
    workspace_id: Identifier
    derivation_id: Identifier
    request: InterpretRequest
    implementation_id: Literal["edi.interpret/1.0"] = "edi.interpret/1.0"
    profile_snapshot: dict[str, JsonValue]
    runtime_versions: dict[str, JsonValue]
    created_at: datetime
    status: Literal["complete", "partial", "failed"]
    artifacts: tuple[Artifact, ...]
    claims: tuple[CheckedClaim, ...]
    native_associations: tuple[NativeAssociation, ...]
    output_sha256: str
    usage: Usage
    error: dict[str, JsonValue] | None = None
    durability: Literal["local-sqlite-full-unqualified"] = "local-sqlite-full-unqualified"


class DerivationReceipt(Record):
    derivation: Derivation
    duplicate: bool


class SubmissionRequest(Record):
    derivation_id: Identifier
    world_request_id: Identifier
    base_revision: int = Field(ge=0)
    consumed: ConsumedEvidence | None = None
    # No admission decision, deletion or implicit rebase is exposed.
