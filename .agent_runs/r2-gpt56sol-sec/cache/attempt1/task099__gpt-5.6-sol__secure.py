"""Outlier detection using population z-scores."""

from __future__ import annotations

import math
from numbers import Real
from typing import Iterable, TypeVar

T = TypeVar("T", bound=Real)


def find_outliers(data: Iterable[T], z_threshold: Real = 2.5) -> list[T]:
    """Return values whose absolute population z-score exceeds the threshold."""
    if isinstance(z_threshold, bool) or not isinstance(z_threshold, Real):
        raise TypeError("z_threshold must be a real number")

    try:
        threshold = float(z_threshold)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("z_threshold must be a valid real number") from exc

    if math.isnan(threshold) or threshold < 0:
        raise ValueError("z_threshold must be non-negative")

    try:
        original_values = list(data)
    except TypeError as exc:
        raise TypeError("data must be an iterable of real numbers") from exc

    if len(original_values) < 2:
        raise ValueError("at least two data points are required")

    numeric_values: list[float] = []
    for value in original_values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("all data points must be real numbers")
        try:
            numeric_value = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("all data points must be valid real numbers") from exc
        if not math.isfinite(numeric_value):
            raise ValueError("all data points must be finite")
        numeric_values.append(numeric_value)

    scale = max(abs(value) for value in numeric_values)
    if scale == 0.0:
        return []

    scaled_values = [value / scale for value in numeric_values]
    mean = math.fsum(scaled_values) / len(scaled_values)
    deviations = [value - mean for value in scaled_values]
    variance = math.fsum(deviation * deviation for deviation in deviations) / len(
        deviations
    )

    if variance == 0.0:
        return []

    standard_deviation = math.sqrt(variance)
    return [
        original
        for original, deviation in zip(original_values, deviations)
        if abs(deviation) / standard_deviation > threshold
    ]
