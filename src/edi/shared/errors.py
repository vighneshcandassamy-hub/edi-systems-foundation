from enum import StrEnum


class ErrorCode(StrEnum):
    INVALID = "malformed-envelope"
    UNSUPPORTED = "unsupported-profile"
    CAPACITY = "capacity-exceeded"
    CONFLICT = "idempotency-or-registration-conflict"
    NOT_FOUND = "not-found"
    DENIED = "scope-denied"
    INTEGRITY = "integrity-mismatch"
    INCOMPLETE = "incomplete-input"
    STORAGE = "storage-unavailable"
    UNKNOWN_COMMIT = "unknown-commit-outcome"
    UNAVAILABLE = "component-unavailable"


class EDIError(Exception):
    def __init__(self, code: ErrorCode, message: str, *, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.retryable = retryable

    def as_dict(self) -> dict:
        return {"status": "error", "code": self.code.value,
                "message": str(self), "retryable": self.retryable}
