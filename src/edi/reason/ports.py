from typing import Protocol

from edi.reason.contracts import Episode, Job, Response
from edi.shared.errors import EDIError, ErrorCode


class InferencePort(Protocol):
    """Future gateway must enforce token/deadline/concurrency and reconcile unknown cost."""
    def complete(self, job: Job, episode: Episode) -> Response: ...


class UnavailableInference:
    def __init__(self, role: str):
        self.role = role

    def complete(self, job: Job, episode: Episode) -> Response:
        raise EDIError(ErrorCode.UNAVAILABLE, f"{self.role} inference is not bound; export/import only")
