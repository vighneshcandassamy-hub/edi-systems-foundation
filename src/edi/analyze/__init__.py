"""C5 owns isolated hypothetical analysis, distinct from observed outcomes."""
from edi.shared.component import DeclaredComponent
from edi.shared.ports import AnalysisPort, UnavailableAdapter


class Analysis(DeclaredComponent):
    def __init__(self, backend: AnalysisPort | None = None):
        super().__init__("C5", ("F50", "F51", "F52", "F53"))
        self.backend = backend if backend is not None else UnavailableAdapter("mathematical backend")
