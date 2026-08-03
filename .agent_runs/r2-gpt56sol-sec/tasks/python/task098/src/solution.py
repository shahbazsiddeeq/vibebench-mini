"""Utilities for calculating Pearson correlation coefficients."""

from __future__ import annotations

import math
from typing import Iterable, Any


def _to_finite_floats(values: Iterable[Any], name: str) -> list[float]:
    if isinstance(values, (str, bytes, bytearray)):
        raise ValueError(f"{name} must be an iterable of finite numbers")

    try:
        items = list(values)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be an iterable of finite numbers") from exc

    result: list[float] = []
    for item in items:
        if isinstance(item, (str, bytes, bytearray, complex)):
            raise ValueError(f"{name} must contain only finite real numbers")
        try:
            number = float(item)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{name} must contain only finite real numbers"
            ) from exc
        if not math.isfinite(number):
            raise ValueError(f"{name} must contain only finite real numbers")
        result.append(number)

    return result


def _centered_values(values: list[float]) -> list[float]:
    scale = max((abs(value) for value in values), default=0.0)
    if scale == 0.0:
        return [0.0] * len(values)

    anchor = values[0] / scale
    offsets = [(value / scale) - anchor for value in values]
    mean_offset = math.fsum(offsets) / len(offsets)
    return [offset - mean_offset for offset in offsets]


def pearson_r(x: Iterable[Any], y: Iterable[Any]) -> float:
    """Return the Pearson correlation coefficient rounded to four decimals.

    Raises:
        ValueError: If the inputs have unequal lengths, contain fewer than two
            values, contain invalid numbers, or either input has zero variance.
    """
    x_values = _to_finite_floats(x, "x")
    y_values = _to_finite_floats(y, "y")

    if len(x_values) != len(y_values):
        raise ValueError("x and y must have equal lengths")
    if len(x_values) < 2:
        raise ValueError("x and y must contain at least two values")

    x_centered = _centered_values(x_values)
    y_centered = _centered_values(y_values)

    x_sum_squares = math.fsum(value * value for value in x_centered)
    y_sum_squares = math.fsum(value * value for value in y_centered)

    if x_sum_squares == 0.0 or y_sum_squares == 0.0:
        raise ValueError("x and y must each have non-zero variance")

    covariance = math.fsum(
        x_value * y_value
        for x_value, y_value in zip(x_centered, y_centered)
    )
    coefficient = covariance / math.sqrt(x_sum_squares * y_sum_squares)

    # Correct negligible floating-point excursions beyond the valid range.
    coefficient = max(-1.0, min(1.0, coefficient))
    rounded = round(coefficient, 4)
    return 0.0 if rounded == 0.0 else rounded
