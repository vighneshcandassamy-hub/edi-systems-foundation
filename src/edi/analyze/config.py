from pathlib import Path

from pydantic import Field

from edi.shared.contracts import Identifier, Record


class AnalysisProfile(Record):
    profile_id: Identifier = "local-analysis-sqlite-v1"
    workspace_id: Identifier = "default"
    database: Path = Field(default_factory=lambda: Path(".local/analyze.sqlite3"))
    max_request_bytes: int = Field(default=256 * 1024, ge=1024)
    max_context_bytes: int = Field(default=1024 * 1024, ge=1024)
    max_result_bytes: int = Field(default=4 * 1024**2, ge=1024)
    max_records: int = Field(default=10000, ge=1)
    max_stored_bytes: int = Field(default=1024**3, ge=1024)
    max_world_records: int = Field(default=128, ge=1, le=256)
    dependency_depth: int = Field(default=4, ge=1, le=16)
    max_output_cells: int = Field(default=100000, ge=1)
    max_rhs_evaluations: int = Field(default=50000, ge=1)
    max_operation_seconds: float = Field(default=30.0, gt=0, le=600)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
