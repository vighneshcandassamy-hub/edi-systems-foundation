from typing import Protocol

from edi.reason.contracts import Episode, Job, Response, ModelBinding
from edi.shared.errors import EDIError, ErrorCode


class InferencePort(Protocol):
    """Configured gateway; explicit dispatch, retained receipt and unknown-cost status."""
    binding: ModelBinding
    def complete(self, job: Job, episode: Episode) -> Response: ...
    def receipt(self, job_id: str) -> dict | None: ...


class UnavailableInference:
    def __init__(self, role: str):
        self.role = role

    def complete(self, job: Job, episode: Episode) -> Response:
        raise EDIError(ErrorCode.UNAVAILABLE, f"{self.role} inference is not bound; export/import only")
