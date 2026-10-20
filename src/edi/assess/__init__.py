"""C6 will own sealed expectations and independent outcome comparisons."""
from edi.shared.component import DeclaredComponent


class Assessment(DeclaredComponent):
    def __init__(self):
        super().__init__("C6", ("F60", "F61", "F62", "F63"))
