"""C7 future authorization/adoption owner. No actuator is installed."""
from edi.shared.component import DeclaredComponent


class Agency(DeclaredComponent):
    def __init__(self):
        super().__init__("C7", ("F70", "F71", "F72", "F73"))
