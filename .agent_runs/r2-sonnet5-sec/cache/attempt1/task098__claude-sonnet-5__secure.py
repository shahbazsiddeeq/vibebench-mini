"""
Pearson Correlation Coefficient module.

Provides a secure, validated implementation of the Pearson correlation
coefficient computation without relying on external libraries.
"""

import math
from numbers import Real
from typing import Sequence


def _validate_numeric_sequence(seq: Sequence, name: str) -> None:
    """Validate that seq is a sequence of real numbers."""
    if not isinstance(seq, (list, tuple)):
        raise ValueError(f"{name} must be a list or tuple of numbers.")
    for item in seq:
        if isinstance(item, bool) or not isinstance(item, Real):
            raise ValueError(f"{name} must contain only numeric values.")
        if isinstance(item, float) and (math.isnan(item) or math.isinf(item)):
            raise ValueError(f"{name} must contain only finite numeric values.")


def pearson_r(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Compute the Pearson correlation coefficient between two numeric sequences.

    Args:
        x: Sequence of numeric values.
        y: Sequence of numeric values.

    Returns:
        The Pearson correlation coefficient rounded to 4 decimal places.

    Raises:
        ValueError: If lengths differ, fewer than 2 elements, non-numeric
                    input, or either sequence has zero variance.
    """
    _validate_numeric_sequence(x, "x")
    _validate_numeric_sequence(y, "y")

    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")

    n = len(x)
    if n < 2:
        raise ValueError("x and y must contain at least 2 elements each.")

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov = 0.0
    var_x = 0.0
    var_y = 0.0

    for xi, yi in zip(x, y):
        dx = xi - mean_x
        dy = yi - mean_y
        cov += dx * dy
        var_x += dx * dx
        var_y += dy * dy

    if var_x == 0 or var_y == 0:
        raise ValueError("Input sequences must have non-zero variance.")

    denominator = math.sqrt(var_x) * math.sqrt(var_y)
    r = cov / denominator

    # Clamp to valid range to avoid floating point drift beyond [-1, 1]
    r = max(-1.0, min(1.0, r))

    return round(r, 4)
