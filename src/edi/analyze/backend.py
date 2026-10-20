"""Optional pinned SciPy ODE adapter; importing this module performs no simulation."""
from importlib.metadata import PackageNotFoundError, version
import math
from time import monotonic

from edi.analyze.compiler import evaluate
from edi.analyze.contracts import Diagnostic, Trajectory
from edi.shared.errors import EDIError, ErrorCode


class Stopped(Exception):
    def __init__(self, reason, *, cancelled=False):
        super().__init__(reason)
        self.cancelled = cancelled


class WorkBudget:
    def __init__(self, profile, cancelled):
        self.profile, self.cancelled = profile, cancelled
        self.started, self.evaluations = monotonic(), 0

    def tick(self, *, rhs=False, force=False):
        if rhs: self.evaluations += 1
        if self.evaluations > self.profile.max_rhs_evaluations:
            raise Stopped("shared scenario RHS evaluation budget exhausted")
        if monotonic() - self.started > self.profile.max_operation_seconds:
            raise Stopped("cooperative scenario wall-time budget exhausted")
        if (force or self.evaluations % 32 == 0) and self.cancelled():
            raise Stopped("C0 requested cancellation or fenced this worker", cancelled=True)


def backend_versions():
    try:
        return {"scipy": version("scipy"), "numpy": version("numpy")}
    except PackageNotFoundError:
        return {"scipy": "unavailable", "numpy": "unavailable"}


def require_backend(solver):
    found = backend_versions()
    if found != {"scipy": solver.scipy_version, "numpy": solver.numpy_version}:
        raise EDIError(ErrorCode.UNAVAILABLE, "pinned SciPy/NumPy backend unavailable; no silent version fallback")


def validate_scenario(program, scenario):
    stocks = {s.symbol: s for s in program.stocks}
    params = {p.symbol: p for p in program.parameters}
    drivers = {p.symbol: p for p in program.drivers}
    if set(scenario.initial_state) != set(stocks):
        raise EDIError(ErrorCode.INVALID, "every stock needs an explicit initial state; extra state is forbidden")
    for symbol, value in scenario.initial_state.items():
        stock = stocks[symbol]
        if (stock.lower is not None and value < stock.lower) or (stock.upper is not None and value > stock.upper):
            raise EDIError(ErrorCode.INVALID, "initial stock violates declared bounds")
    if len(set(v.name for v in scenario.variations)) != len(scenario.variations) or any(v.name == "baseline" for v in scenario.variations):
        raise EDIError(ErrorCode.INVALID, "variant names must be unique; baseline is reserved")
    values = {p.symbol: p.value for p in program.parameters}
    variants = [("baseline", values | scenario.parameters)]
    variants += [(v.name, values | scenario.parameters | v.parameter_values) for v in scenario.variations]
    for name, binding in variants:
        if set(binding) != set(params): raise EDIError(ErrorCode.INVALID, "unknown scenario parameter")
        if name != "baseline" and not next(v for v in scenario.variations if v.name == name).parameter_values:
            raise EDIError(ErrorCode.INVALID, "variant must explicitly change at least one parameter")
        for symbol, value in binding.items():
            if not params[symbol].lower <= value <= params[symbol].upper:
                raise EDIError(ErrorCode.INVALID, "scenario parameter is outside declared domain")
    if len({d.symbol for d in scenario.drivers}) != len(scenario.drivers):
        raise EDIError(ErrorCode.INVALID, "duplicate boundary driver schedule")
    for schedule in scenario.drivers:
        if schedule.symbol not in drivers or schedule.points[0][0] != scenario.start:
            raise EDIError(ErrorCode.INVALID, "driver schedule must name a declared driver and begin at scenario start")
        if any(b[0] <= a[0] for a, b in zip(schedule.points, schedule.points[1:])):
            raise EDIError(ErrorCode.INVALID, "driver change times must be strictly ordered")
        driver = drivers[schedule.symbol]
        if any(not scenario.start <= t <= scenario.end or not driver.lower <= v <= driver.upper for t, v in schedule.points):
            raise EDIError(ErrorCode.INVALID, "driver time/value is outside declared domain")
    if any(c.stock_symbol not in stocks for c in scenario.correspondence) or len({c.stock_symbol for c in scenario.correspondence}) != len(scenario.correspondence):
        raise EDIError(ErrorCode.INVALID, "output correspondence must identify unique modeled stocks")
    return variants


def solve_variant(compiled, scenario, solver, name, parameters, budget):
    require_backend(solver)
    # Lazy optional dependency: no package loading in intake, compile or CLI parsing.
    from scipy.integrate import solve_ivp

    program = compiled.program
    stocks, flows = program.stocks, program.flows
    index = {stock.symbol: i for i, stock in enumerate(stocks)}
    initial = [scenario.initial_state[s.symbol] for s in stocks] + [0.0] * len(flows)
    state = list(initial)
    times, columns, diagnostics = [scenario.start], [list(initial)], []
    scheduled = {d.symbol: d.points for d in scenario.drivers}
    cuts = sorted({scenario.start, scenario.end, *(t for s in scenario.drivers for t, _ in s.points)})
    before, status = budget.evaluations, "completed"
    events = []
    for i, stock in enumerate(stocks):
        for bound, side in ((stock.lower, "lower"), (stock.upper, "upper")):
            if bound is None: continue
            def event(t, y, i=i, bound=bound, side=side):
                return (y[i] - bound if side == "lower" else bound - y[i]) + solver.bound_tolerance
            event.terminal, event.direction = True, -1
            events.append(event)
    try:
        for start, end in zip(cuts, cuts[1:]):
            budget.tick(force=True)
            driver_values = {d.symbol: d.value for d in program.drivers}
            for symbol, points in scheduled.items():
                driver_values[symbol] = next(value for t, value in reversed(points) if t <= start)
            sample_times = sorted({start, end, *(t for t in scenario.output_times if start <= t <= end)})

            def rhs(t, y):
                budget.tick(rhs=True)
                env = dict(parameters) | driver_values | {s.symbol: float(y[i]) for i, s in enumerate(stocks)} | {"time": float(t)}
                rates = evaluate(program, compiled.node_order, env)
                derivative = [0.0] * (len(stocks) + len(flows))
                for j, flow in enumerate(flows):
                    rate = rates[flow.symbol]
                    if rate < 0: raise ValueError("negative flow requires an explicit reverse flow; no automatic clipping")
                    if flow.source is not None: derivative[index[flow.source]] -= rate
                    if flow.sink is not None: derivative[index[flow.sink]] += rate
                    derivative[len(stocks) + j] = rate
                if any(not math.isfinite(x) for x in derivative): raise ValueError("nonfinite stock derivative")
                return derivative

            result = solve_ivp(rhs, (start, end), state, method=solver.method, t_eval=sample_times,
                               rtol=solver.rtol, atol=solver.atol, max_step=solver.max_step,
                               events=events or None, dense_output=False, vectorized=False)
            for t, row in zip(result.t, result.y.T):
                if not math.isfinite(float(t)) or any(not math.isfinite(float(x)) for x in row):
                    raise ValueError("nonfinite solver sample; not retained as a trajectory")
                if float(t) > times[-1]:
                    times.append(float(t)); columns.append([float(x) for x in row])
                for i, stock in enumerate(stocks):
                    if ((stock.lower is not None and float(row[i]) < stock.lower - solver.bound_tolerance)
                            or (stock.upper is not None and float(row[i]) > stock.upper + solver.bound_tolerance)):
                        raise ValueError("reported stock sample violates declared feasibility margin; violating sample retained for diagnosis")
            if result.status == 1:
                event_points = [(float(t), list(map(float, row))) for ts, ys in zip(result.t_events, result.y_events) for t, row in zip(ts, ys)]
                if event_points:
                    t, row = min(event_points, key=lambda point: point[0])
                    if not math.isfinite(t) or any(not math.isfinite(x) for x in row):
                        raise ValueError("nonfinite event state")
                    if t > times[-1]: times.append(t); columns.append(row)
                diagnostics.append(Diagnostic(code="stock-bound-stop", severity="error", message="Declared stock bound reached within the configured numerical margin; no clipping/reallocation applied"))
                status = "partial"
                break
            if not result.success:
                diagnostics.append(Diagnostic(code="solver-failure", severity="error", message=str(result.message)[:8192] or "solver failed"))
                status = "partial"
                break
            state = [float(x) for x in result.y[:, -1]]
            budget.tick(force=True)
    except (Stopped, ValueError, ArithmeticError) as exc:
        status = "partial" if len(times) > 1 else "failed"
        diagnostics.append(Diagnostic(code="cancelled" if isinstance(exc, Stopped) and exc.cancelled else "integration-stopped",
            severity="error", message=str(exc)[:8192] or "numerical integration failed"))
    states = {s.symbol: tuple(row[i] for row in columns) for i, s in enumerate(stocks)}
    transfers = {f.symbol: tuple(row[len(stocks) + j] for row in columns) for j, f in enumerate(flows)}
    residuals = {}
    for stock in stocks:
        expected = sum((1 if f.sink == stock.symbol else -1 if f.source == stock.symbol else 0) * transfers[f.symbol][-1] for f in flows)
        residuals[stock.symbol] = states[stock.symbol][-1] - scenario.initial_state[stock.symbol] - expected
    if any(not math.isfinite(value) for value in residuals.values()):
        raise ValueError("nonfinite balance diagnostic")
    return Trajectory(variant=name, status=status, times=tuple(times), states=states,
        cumulative_transfers=transfers, final_time=times[-1], parameter_values=parameters,
        balance_residuals=residuals, diagnostics=tuple(diagnostics), nfev=budget.evaluations - before)
