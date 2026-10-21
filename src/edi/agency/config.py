from pathlib import Path

from pydantic import Field, model_validator

from edi.shared.contracts import Identifier, Record


class AgencyProfile(Record):
    profile_id: Identifier = "local-agency-research-v1"
    workspace_id: Identifier = "default"
    database: Path = Field(default_factory=lambda: Path(".local/agency.sqlite3"))
    operator_ids: tuple[Identifier, ...] = Field(default=("local-operator",), min_length=1, max_length=16)
    mode: str = Field(default="research-readonly", pattern="^research-readonly$")
    max_request_bytes: int = Field(default=128 * 1024, ge=1024)
    max_document_bytes: int = Field(default=2 * 1024**2, ge=65536)
    max_result_bytes: int = Field(default=1024**2, ge=4096)
    max_page_bytes: int = Field(default=4 * 1024**2, ge=65536)
    max_records: int = Field(default=50000, ge=4)
    max_stored_bytes: int = Field(default=1024**3, ge=65536)
    max_operation_seconds: float = Field(default=15.0, gt=0, le=300)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)

    @model_validator(mode="after")
    def capacities(self):
        if self.max_result_bytes + 16384 > self.max_document_bytes:
            raise ValueError("C7 result allowance requires receipt metadata headroom")
        if self.max_request_bytes > self.max_document_bytes:
            raise ValueError("C7 document capacity must cover the admitted request")
        if len(set(self.operator_ids)) != len(self.operator_ids):
            raise ValueError("duplicate configured operator IDs")
        return self
