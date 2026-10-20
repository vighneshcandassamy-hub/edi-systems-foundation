from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field, JsonValue, model_validator

from edi.shared.contracts import Identifier, Record, TemporalScope


class OriginSpec(Record):
    namespace: Identifier
    native_source_id: Identifier
    epoch: Identifier
    deliverer: Identifier
    channel: Identifier
    adapter: Identifier
    producer: str | None = None
    binding_basis: Literal["reported", "configured", "authenticated"] = "reported"
    binding_evidence_ref: str | None = None
    descriptor: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="after")
    def binding(self):
        if self.binding_basis == "authenticated" and not self.binding_evidence_ref:
            raise ValueError("authenticated binding requires an evidence reference")
        return self


class Origin(Record):
    workspace_id: Identifier
    source_id: Identifier
    origin_ref: Identifier
    registered_at: datetime
    spec: OriginSpec


class Capture(Record):
    origin_ref: Identifier
    idempotency_key: Identifier
    kind: Identifier = "native-bytes"
    media_type: Identifier = "application/octet-stream"
    time: TemporalScope = Field(default_factory=TemporalScope)
    profiles: dict[str, JsonValue] = Field(default_factory=dict)
    critical_profiles: tuple[str, ...] = ()
    origin_class: Literal["external", "generated", "simulation", "unknown"] = "unknown"
    lineage: tuple[str, ...] = ()
    completeness: Literal["complete", "partial", "unknown"] = "unknown"
    expected_bytes: int | None = Field(default=None, ge=0)
    expected_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] | None = None


class Manifest(Record):
    sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    byte_count: int = Field(ge=0)
    chunk_count: int = Field(ge=0)
    chunk_bytes: int = Field(ge=1)
    media_type: Identifier


class Observation(Record):
    # The eight retained envelope fields remain explicit.
    schema_ref: Literal["edi.observation/1.0"] = "edi.observation/1.0"
    record_id: Identifier
    scope_id: Identifier
    kind: Identifier
    receipt_time: datetime
    origin_ref: Identifier
    manifest_ref: Identifier
    profiles: dict[str, JsonValue]
    # Typed implementation extensions, not mandatory ontology/interpretation.
    committed_at: datetime
    commit_position: int = Field(ge=1)
    source_id: Identifier
    capture: Capture
    manifest: Manifest
    durability: Literal["local-sqlite-full-unqualified"] = "local-sqlite-full-unqualified"


class Receipt(Record):
    status: Literal["committed"] = "committed"
    observation: Observation
    duplicate: bool


class ReplayCursor(Record):
    workspace_id: Identifier
    after: int = Field(default=0, ge=0)
    watermark: int = Field(ge=0)
    origin_ref: str | None = None

    @model_validator(mode="after")
    def order(self):
        if self.after > self.watermark:
            raise ValueError("cursor exceeds its snapshot watermark")
        return self


class ReplayPage(Record):
    items: tuple[Observation, ...]
    cursor: ReplayCursor
    has_more: bool


class CommitStatus(Record):
    status: Literal["committed", "not-found"]
    record_id: str | None = None
    commit_position: int | None = None
