"""Utilities for numerical normalization."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any


def _finite_float(value: Any, name: str) -> float:
    """Convert a numeric value to a finite float."""
    if isinstance(value, (str, bytes, bytearray, complex)):
        raise TypeError(f"{name} must contain only real numbers")

    try:
        converted = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise TypeError(f"{name} must contain only real numbers") from None

    if not math.isfinite(converted):
        raise ValueError(f"{name} must contain only finite numbers")

    return converted


def min_max_normalize(
    values: Iterable[float],
    new_min: float = 0.0,
    new_max: float = 1.0,
) -> list[float]:
    """Scale numeric values to the inclusive range ``new_min`` to ``new_max``."""
    if isinstance(values, (str, bytes, bytearray)) or not isinstance(values, Iterable):
        raise TypeError("values must be an iterable of real numbers")

    converted_values = [
        _finite_float(value, "values") for value in values
    ]
    if not converted_values:
        raise ValueError("values must not be empty")

    target_min = _finite_float(new_min, "new_min")
    target_max = _finite_float(new_max, "new_max")

    low = min(converted_values)
    high = max(converted_values)

    if high == low:
        normalized_min = float(round(target_min, 6))
        return [normalized_min for _ in converted_values]

    source_span = high - low
    target_span = target_max - target_min

    result: list[float] = []
    for value in converted_values:
        scaled = target_min + (value - low) / source_span * target_span
        if not math.isfinite(scaled):
            raise ValueError("normalization produced a non-finite result")
        result.append(float(round(scaled, 6)))

    return result
