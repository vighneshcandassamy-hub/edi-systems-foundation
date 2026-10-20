"""Declared limited SI dimensional checker; no quantity conversion or unit inference."""
from decimal import Decimal, InvalidOperation
import re

from edi.shared.contracts import Quantity

_BASE = {
    "1": ((0, 0, 0, 0, 0, 0, 0), "1"),
    "m": ((1, 0, 0, 0, 0, 0, 0), "1"),
    "kg": ((0, 1, 0, 0, 0, 0, 0), "1"),
    "s": ((0, 0, 1, 0, 0, 0, 0), "1"),
    "A": ((0, 0, 0, 1, 0, 0, 0), "1"),
    "K": ((0, 0, 0, 0, 1, 0, 0), "1"),
    "mol": ((0, 0, 0, 0, 0, 1, 0), "1"),
    "cd": ((0, 0, 0, 0, 0, 0, 1), "1"),
    "Hz": ((0, 0, -1, 0, 0, 0, 0), "1"),
    "N": ((1, 1, -2, 0, 0, 0, 0), "1"),
    "Pa": ((-1, 1, -2, 0, 0, 0, 0), "1"),
    "J": ((2, 1, -2, 0, 0, 0, 0), "1"),
    "W": ((2, 1, -3, 0, 0, 0, 0), "1"),
    "mm": ((1, 0, 0, 0, 0, 0, 0), "0.001"),
    "cm": ((1, 0, 0, 0, 0, 0, 0), "0.01"),
    "km": ((1, 0, 0, 0, 0, 0, 0), "1000"),
    "g": ((0, 1, 0, 0, 0, 0, 0), "0.001"),
    "ms": ((0, 0, 1, 0, 0, 0, 0), "0.001"),
}


def _dimension(unit: str):
    if not unit or len(unit) > 128:
        return None
    tokens = re.split(r"([*/])", unit)
    if len(tokens) > 31:
        return None
    dims, scale, sign = [0] * 7, Decimal(1), 1
    for index, token in enumerate(tokens):
        if index % 2:
            sign = -1 if token == "/" else 1
            continue
        match = re.fullmatch(r"([A-Za-z]+|1)(?:\^(-?[0-8]))?", token.strip())
        if match is None or match[1] not in _BASE:
            return None
        power = int(match[2] or 1) * sign
        vector, factor = _BASE[match[1]]
        dims = [a + power * b for a, b in zip(dims, vector)]
        scale *= Decimal(factor) ** power
    return dims, str(scale)


def check_quantity(quantity: Quantity | None, expected_unit: str | None) -> dict:
    prefix = {"checker": "edi.limited-si/1.0", "conversion_performed": False,
              "source_unit_meaning": "caller-declared; not semantically verified"}
    if quantity is None or quantity.status != "known":
        return prefix | {"status": "unknown"}
    if quantity.scale != "cardinal":
        return prefix | {"status": "not-applicable", "reason": "no arithmetic on non-cardinal scale"}
    value = str(quantity.value)
    try:
        if isinstance(quantity.value, bool) or len(value) > 256 or not Decimal(value).is_finite():
            raise InvalidOperation
    except InvalidOperation:
        return prefix | {"status": "invalid-number", "reason": "cardinal value is not a supported finite numeric scalar"}
    if quantity.unit is None:
        return prefix | {"status": "unknown"}
    source = _dimension(quantity.unit)
    expected = _dimension(expected_unit) if expected_unit is not None else None
    if source is None or (expected_unit is not None and expected is None):
        return prefix | {"status": "unsupported", "reason": "outside declared limited SI grammar"}
    status = "dimension-known" if expected is None else "compatible" if source[0] == expected[0] else "incompatible"
    return prefix | {"status": status, "dimensions_m_kg_s_A_K_mol_cd": source[0],
                     "source_scale": source[1], "expected_scale": expected[1] if expected else None}
