"""Finite scalar scoring and descriptive calibration; no implicit iid inference."""
import json
import math

from edi.assess.contracts import Measurement


def parse_measurement(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result: raise ValueError("duplicate JSON measurement key")
            result[key] = value
        return result
    def constant(value): raise ValueError("nonfinite JSON measurement token")
    decoded = json.loads(data.decode("utf-8", errors="strict"), object_pairs_hook=pairs, parse_constant=constant)
    return Measurement.model_validate_json(json.dumps(decoded, allow_nan=False, ensure_ascii=False))


def scores(point, observation):
    value = observation.value
    if point.case.interpretation == "point" and isinstance(value, bool):
        raise ValueError("boolean outcome cannot be silently interpreted as cardinal measurement")
    actual = float(value)
    if point.case.interpretation == "bernoulli-probability" and actual not in (0.0, 1.0):
        raise ValueError("Brier loss requires a binary outcome")
    error = point.predicted - actual
    result = {"signed_error": error, "absolute_error": abs(error), "squared_error": error * error}
    key = "absolute_error"
    if point.case.interpretation == "bernoulli-probability":
        result["brier_loss"] = result["squared_error"]
        key = "brier_loss"
    if any(not math.isfinite(x) for x in result.values()):
        raise ValueError("score overflow; no clipping or fabricated finite score")
    return result, result[key] <= point.case.score_limit


def summaries(results, rule):
    eligible = [r for r in results if r.status == "scored"]
    groups = {}
    for row in eligible:
        key = row.point.case.interpretation + ":" + row.point.unit.symbol
        groups.setdefault(key, []).append(row)
    metrics = {}
    for key, rows in groups.items():
        # Scaling before fsum avoids overflowing the sum of finite observations.
        count = len(rows)
        metrics[key] = {"count": count,
            "mean_signed_error": math.fsum(r.scores["signed_error"] / count for r in rows),
            "mean_absolute_error": math.fsum(r.scores["absolute_error"] / count for r in rows),
            "mean_squared_error": math.fsum(r.scores["squared_error"] / count for r in rows),
            "unique_source_count": len({r.source_id for r in rows}),
            "declared_dependence_groups": len({r.point.case.declared_dependence_group for r in rows})}
        if rows[0].point.case.interpretation == "bernoulli-probability":
            metrics[key]["mean_brier_loss"] = metrics[key]["mean_squared_error"]
    binary = [r for r in eligible if r.point.case.interpretation == "bernoulli-probability"]
    bins = []
    for i, (lower, upper) in enumerate(zip(rule.calibration_edges, rule.calibration_edges[1:])):
        rows = [r for r in binary if lower <= r.point.predicted < upper or (i == len(rule.calibration_edges) - 2 and r.point.predicted == upper)]
        bins.append({"lower": lower, "upper": upper, "count": len(rows),
            "mean_probability": math.fsum(r.point.predicted / len(rows) for r in rows) if rows else None,
            "observed_fraction": math.fsum(float(r.observation.value) / len(rows) for r in rows) if rows else None,
            "unique_sources": len({r.source_id for r in rows})})
    return {"planned_count": len(results), "scored_count": len(eligible),
        "unscored_count": len(results) - len(eligible),
        "coverage_fraction": len(eligible) / len(results) if results else 0.0,
        "by_quantity_and_interpretation": metrics, "descriptive_calibration_bins": bins,
        "declared_limit_result": ("incomplete" if len(eligible) != len(results) else "within-declared-limits"
                                  if all(r.within_declared_limit for r in eligible) else "outside-declared-limits"),
        "dependence_limit": "source/group counts are not effective independent sample sizes; no iid confidence or skill claim"}
