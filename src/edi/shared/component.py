from edi.shared.contracts import Capability, CommandEnvelope, Owner, ResultEnvelope
from edi.shared.errors import EDIError, ErrorCode


class DeclaredComponent:
    """Visible missing capability. Never emits placeholder successful results."""
    def __init__(self, owner: Owner, functions: tuple[str, ...]):
        self.capability = Capability(
            owner=owner, functions=functions, state="declared-unavailable",
            details="Port declared; implementation scheduled for a later component increment",
        )

    def handle(self, command: CommandEnvelope) -> ResultEnvelope:
        raise EDIError(ErrorCode.UNAVAILABLE,
                       f"{self.capability.owner} is declared but not implemented")
