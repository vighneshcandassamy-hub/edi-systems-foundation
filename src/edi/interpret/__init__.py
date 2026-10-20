"""C2 owns derivations and correspondence proposals; never C1 evidence writes."""
from edi.shared.component import DeclaredComponent


class Interpretation(DeclaredComponent):
    def __init__(self):
        super().__init__("C2", ("F20", "F21", "F22", "F23"))
