"""Utilities for calculating Pearson correlation."""

from math import fsum, sqrt
from typing import Iterable


def pearson_r(x: Iterable[float], y: Iterable[float]) -> float:
    """Return the Pearson correlation coefficient rounded to four decimals.

    Raises:
        ValueError: If the inputs have different lengths, contain fewer than
            two elements, or either input has zero variance.
    """
    x_values = list(x)
    y_values = list(y)

    if len(x_values) != len(y_values):
        raise ValueError("x and y must have the same length")
    if len(x_values) < 2:
        raise ValueError("x and y must contain at least two elements")

    count = len(x_values)
    mean_x = fsum(x_values) / count
    mean_y = fsum(y_values) / count

    deviations_x = [value - mean_x for value in x_values]
    deviations_y = [value - mean_y for value in y_values]

    sum_squares_x = fsum(value * value for value in deviations_x)
    sum_squares_y = fsum(value * value for value in deviations_y)

    if sum_squares_x == 0 or sum_squares_y == 0:
        raise ValueError("x and y must have non-zero variance")

    denominator = sqrt(sum_squares_x) * sqrt(sum_squares_y)
    correlation = fsum(
        dx * dy for dx, dy in zip(deviations_x, deviations_y)
    ) / denominator

    # Guard against tiny floating-point excursions outside the valid range.
    correlation = max(-1.0, min(1.0, correlation))
    result = round(correlation, 4)
    return 0.0 if result == 0 else result
