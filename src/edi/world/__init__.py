"""C3 is the sole future model-admission/revision authority."""
from edi.shared.component import DeclaredComponent


class World(DeclaredComponent):
    def __init__(self):
        super().__init__("C3", ("F30", "F31", "F32", "F33"))
