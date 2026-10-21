from pathlib import Path

from pydantic import Field

from edi.shared.contracts import Identifier, Record


class WorldProfile(Record):
    profile_id: Identifier = "local-world-sqlite-v1"
    database: Path = Path(".local/world.sqlite3")
    workspace_id: Identifier = "default"
    max_patch_bytes: int = Field(default=1024 * 1024, ge=1024)
    max_record_bytes: int = Field(default=64 * 1024, ge=1024)
    max_operations: int = Field(default=64, ge=1, le=1024)
    max_refs_per_record: int = Field(default=128, ge=1, le=4096)
    max_evidence_per_patch: int = Field(default=256, ge=1)
    max_versions: int = Field(default=1_000_000, ge=1)
    max_stored_bytes: int = Field(default=1024**3, ge=1024)
    max_consumers: int = Field(default=1000, ge=1)
    max_page_records: int = Field(default=100, ge=1, le=1000)
    max_dependency_nodes: int = Field(default=256, ge=1, le=10000)
    max_dependency_edges: int = Field(default=1024, ge=1, le=20000)
    max_dependency_depth: int = Field(default=8, ge=1, le=32)
    max_concurrent_operations: int = Field(default=4, ge=1, le=64)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    max_sql_seconds: float = Field(default=2.0, gt=0, le=60)
    max_sql_steps: int = Field(default=1_000_000, ge=1000)
    max_commit_seconds: float = Field(default=10.0, gt=0, le=300)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
