"""Population z-score normalization utilities."""

from __future__ import annotations

import math
from collections.abc import Iterable
from numbers import Real

__all__ = ["z_scores"]


def z_scores(data: Iterable[Real]) -> list[float]:
    """Return the population z-score of each value in *data*.

    Raises:
        TypeError: If data is not iterable or contains non-real values.
        ValueError: If fewer than two values are supplied, a value is not
            finite, or the population standard deviation is zero.
    """
    if isinstance(data, (str, bytes, bytearray)):
        raise TypeError("data must be an iterable of real numbers")

    try:
        raw_values = list(data)
    except TypeError:
        raise TypeError("data must be an iterable of real numbers") from None

    if len(raw_values) < 2:
        raise ValueError("at least two data points are required")

    values: list[float] = []
    for value in raw_values:
        if not isinstance(value, Real):
            raise TypeError("all data points must be real numbers")
        try:
            converted = float(value)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("all data points must be finite") from None
        if not math.isfinite(converted):
            raise ValueError("all data points must be finite")
        values.append(converted)

    # Scaling first avoids overflow when calculating the mean and variance.
    scale = max(abs(value) for value in values)
    if scale == 0.0:
        raise ValueError("population standard deviation must be nonzero")

    scaled = [value / scale for value in values]
    mean = math.fsum(scaled) / len(scaled)
    deviations = [value - mean for value in scaled]
    standard_deviation = math.hypot(*deviations) / math.sqrt(len(deviations))

    if standard_deviation == 0.0:
        raise ValueError("population standard deviation must be nonzero")

    return [deviation / standard_deviation for deviation in deviations]
