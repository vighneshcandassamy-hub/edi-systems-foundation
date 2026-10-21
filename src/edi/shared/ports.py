"""Replaceable dependencies. Declared ports are not installed integrations."""
from typing import Protocol

from edi.shared.contracts import CommandEnvelope, ResultEnvelope
from edi.shared.errors import EDIError, ErrorCode


class ComponentPort(Protocol):
    def handle(self, command: CommandEnvelope) -> ResultEnvelope: ...


class ModelPort(Protocol):
    def propose(self, command: CommandEnvelope) -> ResultEnvelope: ...


class AnalysisPort(Protocol):
    def execute(self, command: CommandEnvelope) -> ResultEnvelope: ...


class UnavailableAdapter:
    def __init__(self, name: str):
        self.name = name

    def _fail(self):
        raise EDIError(ErrorCode.UNAVAILABLE, f"{self.name} has no installed adapter")

    def handle(self, command: CommandEnvelope) -> ResultEnvelope:
        return self._fail()

    def propose(self, command: CommandEnvelope) -> ResultEnvelope:
        return self._fail()

    def execute(self, command: CommandEnvelope) -> ResultEnvelope:
        return self._fail()
