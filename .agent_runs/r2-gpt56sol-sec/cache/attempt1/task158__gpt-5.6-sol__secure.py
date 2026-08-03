"""Simple ordinary least-squares linear regression."""

from __future__ import annotations

import math
from numbers import Real
from typing import Sequence


def linear_regression(
    xs: Sequence[Real], ys: Sequence[Real]
) -> tuple[float, float]:
    """Fit and return ``(slope, intercept)`` rounded to six decimal places."""
    if isinstance(xs, (str, bytes)) or isinstance(ys, (str, bytes)):
        raise ValueError("xs and ys must be numeric sequences")

    try:
        x_values = list(xs)
        y_values = list(ys)
    except TypeError:
        raise ValueError("xs and ys must be numeric sequences") from None

    if len(x_values) != len(y_values):
        raise ValueError("xs and ys must have the same length")
    if len(x_values) < 2:
        raise ValueError("at least two points are required")

    if any(isinstance(value, bool) or not isinstance(value, Real) for value in x_values):
        raise ValueError("xs must contain only real numbers")
    if any(isinstance(value, bool) or not isinstance(value, Real) for value in y_values):
        raise ValueError("ys must contain only real numbers")

    try:
        x_floats = [float(value) for value in x_values]
        y_floats = [float(value) for value in y_values]
    except (TypeError, ValueError, OverflowError):
        raise ValueError("values must be finite real numbers") from None

    if not all(math.isfinite(value) for value in x_floats + y_floats):
        raise ValueError("values must be finite real numbers")

    count = len(x_floats)
    mean_x = math.fsum(x_floats) / count
    mean_y = math.fsum(y_floats) / count

    x_deviations = [x - mean_x for x in x_floats]
    denominator = math.fsum(deviation * deviation for deviation in x_deviations)

    if denominator == 0.0:
        raise ValueError("slope is undefined when all x values are identical")

    numerator = math.fsum(
        x_deviation * (y - mean_y)
        for x_deviation, y in zip(x_deviations, y_floats)
    )
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x

    if not math.isfinite(slope) or not math.isfinite(intercept):
        raise ValueError("regression result is not finite")

    return float(round(slope, 6)), float(round(intercept, 6))
