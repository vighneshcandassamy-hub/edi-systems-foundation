from pathlib import Path

from pydantic import Field

from edi.shared.contracts import Identifier, Record


class LocalProfile(Record):
    profile_id: Identifier = "local-sqlite-v1"
    database: Path = Path(".local/edi.sqlite3")
    workspace_id: Identifier = "default"
    max_chunk_bytes: int = Field(default=1024 * 1024, ge=1, le=8 * 1024 * 1024)
    max_record_bytes: int = Field(default=64 * 1024 * 1024, ge=0)
    max_chunks_per_record: int = Field(default=4096, ge=1)
    max_metadata_bytes: int = Field(default=64 * 1024, ge=1024)
    max_records: int = Field(default=1_000_000, ge=1)
    max_origins: int = Field(default=10_000, ge=1)
    max_consumers: int = Field(default=1_000, ge=1)
    max_payload_bytes: int = Field(default=4 * 1024**3, ge=0)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
    max_page_records: int = Field(default=100, ge=1, le=1000)
    max_concurrent_operations: int = Field(default=4, ge=1, le=64)
    max_read_bytes: int = Field(default=4 * 1024**2, ge=1)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    max_ingest_seconds: float = Field(default=30.0, gt=0, le=3600)
    max_backup_seconds: float = Field(default=300.0, gt=0, le=3600)
