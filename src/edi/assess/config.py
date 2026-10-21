from pathlib import Path

from pydantic import Field

from edi.shared.contracts import Identifier, Record


class AssessmentProfile(Record):
    profile_id: Identifier = "local-assessment-sqlite-v1"
    workspace_id: Identifier = "default"
    database: Path = Field(default_factory=lambda: Path(".local/assess.sqlite3"))
    max_request_bytes: int = Field(default=256 * 1024, ge=1024)
    max_document_bytes: int = Field(default=4 * 1024**2, ge=32768)
    max_context_bytes: int = Field(default=8 * 1024**2, ge=32768)
    max_records: int = Field(default=50000, ge=2)
    max_stored_bytes: int = Field(default=1024**3, ge=32768)
    max_origins: int = Field(default=8, ge=1, le=16)
    max_input_refs: int = Field(default=256, ge=1, le=1024)
    max_scan_records: int = Field(default=2000, ge=1, le=100000)
    page_size: int = Field(default=100, ge=1, le=100)
    max_payload_bytes: int = Field(default=16384, ge=128, le=65536)
    max_total_read_bytes: int = Field(default=1024**2, ge=128)
    max_page_bytes: int = Field(default=8 * 1024**2, ge=32768)
    max_operation_seconds: float = Field(default=15.0, gt=0, le=300)
    minimum_lead_seconds: float = Field(default=1.0, ge=0)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
