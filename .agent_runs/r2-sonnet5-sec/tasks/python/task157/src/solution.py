"""
Min-Max Normalization
======================

Provides `min_max_normalize`, a function that rescales a list of numeric
values into a target range using min-max scaling.

This module performs strict input validation to avoid unexpected behavior
or leaking internal error details, and relies solely on the Python
standard library.
"""

from numbers import Real
from typing import List, Sequence


def _validate_values(values: Sequence) -> None:
    """Validate that `values` is a non-empty sequence of real numbers."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple of numbers")
    if len(values) == 0:
        raise ValueError("values must not be empty")
    for item in values:
        if isinstance(item, bool) or not isinstance(item, Real):
            raise TypeError("all elements of values must be numeric (int or float)")


def _validate_bound(name: str, value) -> float:
    """Validate that a bound argument is numeric and return it as a float."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a numeric value")
    return float(value)


def min_max_normalize(
    values: Sequence[Real],
    new_min: Real = 0.0,
    new_max: Real = 1.0,
) -> List[float]:
    """
    Rescale a list of numbers to a target range using min-max scaling.

    For each element x, the scaled value is:
        new_min + (x - lo) / (hi - lo) * (new_max - new_min)
    where lo = min(values) and hi = max(values).

    If hi == lo (constant series, including single-element lists), every
    output value equals float(new_min) instead of dividing by zero.

    Args:
        values: A non-empty list/tuple of real numbers to normalize.
        new_min: The lower bound of the target range (default 0.0).
        new_max: The upper bound of the target range (default 1.0).

    Returns:
        A new list of floats, each rounded to 6 decimal places. The input
        list is never modified.

    Raises:
        ValueError: If `values` is empty.
        TypeError: If `values` or the bounds are not of the expected types.
    """
    _validate_values(values)
    new_min_f = _validate_bound("new_min", new_min)
    new_max_f = _validate_bound("new_max", new_max)

    lo = min(values)
    hi = max(values)

    if hi == lo:
        constant = round(float(new_min_f), 6)
        return [constant for _ in values]

    span = float(hi - lo)
    target_span = new_max_f - new_min_f

    result: List[float] = []
    for x in values:
        scaled = new_min_f + (float(x) - float(lo)) / span * target_span
        result.append(round(float(scaled), 6))

    return result
