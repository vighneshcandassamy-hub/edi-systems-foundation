"""No eval/exec/code generation: compile a flat, typed stock/flow expression DAG."""
import math
import re

from edi.analyze.contracts import Program
from edi.shared.errors import EDIError, ErrorCode

IR_KEY = "edi_ir_v1"
COMPILER = "edi.stock-flow-compiler/1.0"
SI = {"1": {}, "s": {"s": 1}, "kg": {"kg": 1}, "m": {"m": 1},
      "A": {"A": 1}, "K": {"K": 1}, "mol": {"mol": 1}, "cd": {"cd": 1},
      "Hz": {"s": -1}, "m/s": {"m": 1, "s": -1}, "kg/s": {"kg": 1, "s": -1},
      "1/s": {"s": -1}, "J": {"kg": 1, "m": 2, "s": -2},
      "W": {"kg": 1, "m": 2, "s": -3}}


def unsupported(message):
    raise EDIError(ErrorCode.UNSUPPORTED, message)


def dimension(unit):
    parsed = {}
    tokens = re.split(r"([*/])", unit.symbol)
    valid, sign = len(tokens) <= 31, 1
    for i, token in enumerate(tokens):
        if i % 2:
            sign = -1 if token == "/" else 1
            continue
        match = re.fullmatch(r"([A-Za-z]+|1)(?:\^(-?[0-8]))?", token)
        if match is None or match[1] not in SI:
            valid = False
            break
        for key, power in SI[match[1]].items():
            parsed[key] = parsed.get(key, 0) + sign * int(match[2] or 1) * power
    parsed = {key: power for key, power in parsed.items() if power}
    if valid:
        if unit.dimensions != parsed:
            unsupported(f"unit {unit.symbol} contradicts the pinned coherent-SI definition")
    elif unit.basis != "declared-domain" or not any(key.startswith("domain:") for key in unit.dimensions):
        unsupported(f"unit {unit.symbol} is outside this SI grammar; explicit domain units require declared-domain basis")
    if any(key not in ("m", "kg", "s", "A", "K", "mol", "cd") and not key.startswith("domain:") for key in unit.dimensions):
        unsupported("dimension keys must be SI bases or explicit domain: names")
    return tuple(sorted(unit.dimensions.items()))


def combine(a, b, sign=1):
    result = dict(a)
    for key, power in b:
        result[key] = result.get(key, 0) + sign * power
    return tuple(sorted((key, power) for key, power in result.items() if power))


def compile_program(program: Program):
    if program.required_capabilities:
        unsupported("unsupported capabilities: " + ", ".join(program.required_capabilities))
    variables = [x.symbol for x in (*program.stocks, *program.parameters, *program.drivers)]
    flows = [x.symbol for x in program.flows]
    if len(set(variables + flows + ["time"])) != len(variables + flows) + 1:
        unsupported("stock/parameter/driver/flow symbols must be globally unique; time is reserved")
    unit_names = {}

    def checked(unit):
        dims = dimension(unit)
        if unit.symbol in unit_names and unit_names[unit.symbol] != dims:
            unsupported("one unit symbol has incompatible dimensions")
        unit_names[unit.symbol] = dims
        return dims

    units = {x.symbol: checked(x.unit) for x in (*program.stocks, *program.parameters, *program.drivers)}
    units["time"] = (("s", 1),)
    nodes = {node.node_id: node for node in program.nodes}
    if len(nodes) != len(program.nodes):
        unsupported("duplicate expression node ID")
    dimensions, order, pending = {}, [], dict(nodes)
    while pending:
        progressed = False
        for node_id, node in tuple(pending.items()):
            if any(ref not in nodes for ref in node.inputs):
                unsupported("expression refers to missing node")
            if any(ref not in dimensions for ref in node.inputs):
                continue
            op, inputs = node.operator, node.inputs
            arity = 0 if op in ("constant", "read") else 1 if op in ("negate", "lookup") else 2
            if len(inputs) != arity:
                unsupported(f"wrong arity for {op}")
            if op == "constant":
                if node.value is None or node.unit is None or node.symbol is not None:
                    unsupported("constant requires a finite value/unit and no symbol")
                dims = checked(node.unit)
            elif op == "read":
                if node.symbol not in units or node.value is not None or node.unit is not None:
                    unsupported("read must name a declared stock/parameter/driver/time symbol only")
                dims = units[node.symbol]
            else:
                if node.value is not None or node.unit is not None or node.symbol is not None:
                    unsupported("operator cannot carry an ignored literal, symbol or unit")
                a = dimensions[inputs[0]]
                if op in ("add", "subtract", "min", "max"):
                    if a != dimensions[inputs[1]]:
                        unsupported("add/subtract/min/max require exactly compatible dimensions")
                    dims = a
                elif op in ("multiply", "divide"):
                    dims = combine(a, dimensions[inputs[1]], -1 if op == "divide" else 1)
                elif op == "negate":
                    dims = a
                else:
                    if node.x_unit is None or node.y_unit is None or len(node.points) < 2:
                        unsupported("lookup needs x/y units and at least two ordered finite points")
                    if a != checked(node.x_unit) or any(b[0] <= a[0] for a, b in zip(node.points, node.points[1:])):
                        unsupported("lookup x dimension or strict table ordering invalid")
                    dims = checked(node.y_unit)
            if op != "lookup" and (node.points or node.x_unit is not None or node.y_unit is not None or node.extrapolation != "error"):
                unsupported("lookup-only fields cannot be silently ignored")
            dimensions[node_id] = dims
            order.append(node_id)
            del pending[node_id]
            progressed = True
        if not progressed:
            unsupported("algebraic expression cycle/DAE requires an unsupported solver")
    stocks = {s.symbol: s for s in program.stocks}
    for flow in program.flows:
        if flow.rate_node not in dimensions or (flow.source is None and flow.sink is None) or flow.source == flow.sink:
            unsupported("flow needs a rate node and one or two distinct stock endpoints")
        if any(symbol not in stocks for symbol in (flow.source, flow.sink) if symbol is not None):
            unsupported("flow endpoint is not a declared stock")
        sides = [units[symbol] for symbol in (flow.source, flow.sink) if symbol is not None]
        if len(sides) == 2 and sides[0] != sides[1]:
            unsupported("identity transfer needs matching stock units; conversion/loss laws are unsupported")
        if dimensions[flow.rate_node] != combine(sides[0], (("s", 1),), -1):
            unsupported("flow rate must have stock quantity per second dimensions")
    if len({(s.world_ref.record_id, s.world_ref.version) for s in program.stocks}) != len(program.stocks):
        unsupported("one C3 stock cannot be counted as two state variables")
    if len({(f.world_ref.record_id, f.world_ref.version) for f in program.flows}) != len(program.flows):
        unsupported("one C3 flow cannot be duplicated as separate transfers")
    return tuple(order)


def check_world(program, records, mechanism):
    """Validate declared native participants and reject unrepresented dynamics."""
    response = mechanism.representation.structure
    if response.delays or response.capacities or response.domains:
        unsupported("native delay/capacity/domain descriptors require a separately supported mapping; not ignored")
    if response.parameters and response.parameters != {p.symbol: p.value for p in program.parameters}:
        unsupported("native parameter descriptors conflict with, or are not mapped by, the IR")
    declared = {(p.ref.record_id, p.ref.version) for p in response.participants}
    expected = {(p.world_ref.record_id, p.world_ref.version) for p in (*program.stocks, *program.flows)}
    if declared != expected:
        unsupported("joint response participants must exactly match declared IR stocks/flows; no hidden native input is ignored")
    for spec in (*program.stocks, *program.flows):
        key = (spec.world_ref.record_id, spec.world_ref.version)
        if key not in declared:
            unsupported("IR participant is absent from the native joint response relationship")
        native = records[spec.world_ref.record_id].representation.structure
        if hasattr(spec, "unit"):
            if native.family != "stock" or native.quantity.scale != "cardinal" or native.quantity.unit != spec.unit.symbol:
                unsupported("IR stock must match a cardinal native stock with the same declared coherent unit")
            if native.bounds:
                if set(native.bounds) - {"lower", "upper"}:
                    unsupported("unmapped native stock bound descriptors")
                for key in ("lower", "upper"):
                    if key in native.bounds and (type(native.bounds[key]) not in (int, float) or native.bounds[key] != getattr(spec, key)):
                        unsupported("IR stock bounds differ from native bounds")
            if native.reserve_and_access:
                unsupported("native stock reserve/access policy requires a supported allocation mapping")
            for attribute, side in (("inflows", "sink"), ("outflows", "source")):
                expected_flows = {(flow.world_ref.record_id, flow.world_ref.version) for flow in program.flows if getattr(flow, side) == spec.symbol}
                if {(ref.record_id, ref.version) for ref in getattr(native, attribute)} != expected_flows:
                    unsupported("native stock inflow/outflow inventory differs from declared IR incidence")
        else:
            if native.family != "flow-process":
                unsupported("IR flow must reference a native flow-process")
            if native.pending_commitments or native.prerequisites or native.resource_use or native.transformation:
                unsupported("pending commitments/prerequisites/resource allocation/transformations are unsupported; never discarded")
            if native.response is not None and (native.response.record_id != mechanism.representation.record_id or native.response.version != mechanism.version):
                unsupported("native flow names a different governing response version")
            if native.rate is not None:
                endpoint = next(s for s in program.stocks if s.symbol == (spec.source or spec.sink))
                if native.rate.scale != "cardinal" or native.rate.unit != endpoint.unit.symbol + "/s":
                    unsupported("native rate metadata requires the profile's exact coherent stock-unit/s declaration")
            wanted = set()
            for symbol, role, direction in ((spec.source, "source", "out"), (spec.sink, "sink", "in")):
                if symbol is not None:
                    stock = next(s for s in program.stocks if s.symbol == symbol)
                    wanted.add((stock.world_ref.record_id, stock.world_ref.version, role, direction))
            actual = {(p.ref.record_id, p.ref.version, p.role, p.direction) for p in native.participants}
            if actual != wanted:
                unsupported("native flow source/out and sink/in participants must match the IR endpoints exactly")


def evaluate(program, order, environment):
    values, nodes = {}, {node.node_id: node for node in program.nodes}
    for node_id in order:
        node = nodes[node_id]
        args = [values[ref] for ref in node.inputs]
        op = node.operator
        if op == "constant": value = node.value
        elif op == "read": value = environment[node.symbol]
        elif op == "add": value = args[0] + args[1]
        elif op == "subtract": value = args[0] - args[1]
        elif op == "multiply": value = args[0] * args[1]
        elif op == "divide":
            if args[1] == 0: raise ValueError("zero denominator in mechanism domain")
            value = args[0] / args[1]
        elif op == "negate": value = -args[0]
        elif op == "min": value = min(args)
        elif op == "max": value = max(args)
        else:
            x, points = args[0], node.points
            if x < points[0][0] or x > points[-1][0]:
                if node.extrapolation != "clamp": raise ValueError("lookup outside declared domain")
                value = points[0][1] if x < points[0][0] else points[-1][1]
            else:
                value = points[-1][1]
                for left, right in zip(points, points[1:]):
                    if left[0] <= x <= right[0]:
                        value = left[1] + (right[1] - left[1]) * (x - left[0]) / (right[0] - left[0])
                        break
        value = float(value)
        if not math.isfinite(value): raise ValueError("nonfinite mechanism result")
        values[node_id] = value
    return {flow.symbol: values[flow.rate_node] for flow in program.flows}
