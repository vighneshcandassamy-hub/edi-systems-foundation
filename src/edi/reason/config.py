from pathlib import Path

from pydantic import Field

from edi.reason.contracts import ModelBinding
from edi.shared.contracts import Identifier, Record


class ReasoningProfile(Record):
    profile_id: Identifier = "local-reason-sqlite-v1"
    workspace_id: Identifier = "default"
    database: Path = Field(default_factory=lambda: Path(".local/reason.sqlite3"))
    student: ModelBinding = Field(default_factory=ModelBinding)
    teacher: ModelBinding = Field(default_factory=ModelBinding)
    max_request_bytes: int = Field(default=256 * 1024, ge=1024)
    max_context_bytes: int = Field(default=128 * 1024, ge=1024)
    max_episode_bytes: int = Field(default=1024 * 1024, ge=1024)
    max_commands: int = Field(default=50000, ge=1)
    max_episodes: int = Field(default=10000, ge=1)
    max_stored_bytes: int = Field(default=512 * 1024**2, ge=1024)
    max_frontier: int = Field(default=128, ge=1, le=256)
    max_outbox: int = Field(default=256, ge=1, le=1024)
    max_submissions: int = Field(default=16, ge=1, le=64)
    max_operation_seconds: float = Field(default=10.0, gt=0, le=120)
    writer_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    min_free_disk_bytes: int = Field(default=256 * 1024**2, ge=0)
