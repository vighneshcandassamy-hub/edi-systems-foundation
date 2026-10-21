from pathlib import Path

from pydantic import Field

from edi.shared.contracts import Identifier, Record


class InterpretationProfile(Record):
    profile_id: Identifier = "local-interpret-sqlite-v1"
    workspace_id: Identifier = "default"
    database: Path = Path(".local/interpret.sqlite3")
    max_request_bytes: int = Field(default=128 * 1024, ge=1024)
    max_input_bytes: int = Field(default=8 * 1024**2, ge=1)
    max_output_bytes: int = Field(default=4 * 1024**2, ge=1024)
    max_text_characters: int = Field(default=262144, ge=1)
    read_chunk_bytes: int = Field(default=65536, ge=1, le=1024**2)
    max_nodes: int = Field(default=4096, ge=1, le=100000)
    max_depth: int = Field(default=32, ge=1, le=64)
    max_cells: int = Field(default=16384, ge=1)
    max_native_associations: int = Field(default=32, ge=0, le=128)
    max_derivations: int = Field(default=100000, ge=1)
    max_stored_bytes: int = Field(default=1024**3, ge=1024)
    max_concurrent_operations: int = Field(default=2, ge=1, le=16)
    max_operation_seconds: float = Field(default=10.0, gt=0, le=300)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
