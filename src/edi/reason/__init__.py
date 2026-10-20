"""C4 proposes hypotheses/inquiries; no model admission or external execution."""
from edi.shared.component import DeclaredComponent
from edi.shared.ports import ModelPort, UnavailableAdapter


class Reasoning(DeclaredComponent):
    def __init__(self, student: ModelPort | None = None, teacher: ModelPort | None = None):
        super().__init__("C4", ("F40", "F41", "F42", "F43"))
        self.student = student if student is not None else UnavailableAdapter("student/vLLM")
        self.teacher = teacher if teacher is not None else UnavailableAdapter("teacher")
