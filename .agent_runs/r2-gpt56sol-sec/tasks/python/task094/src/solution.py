"""Descriptive statistics utilities."""

from __future__ import annotations

import math
import statistics
from collections import Counter
from collections.abc import Iterable
from numbers import Real
from typing import Any


def describe(data: Iterable[Real]) -> dict[str, Any]:
    """Return descriptive statistics for a non-empty numeric iterable.

    Raises:
        ValueError: If *data* is empty.
        TypeError: If *data* is not iterable or contains non-real values.
        ValueError: If any value is NaN or infinite.
    """
    if isinstance(data, (str, bytes, bytearray)):
        raise TypeError("data must be an iterable of real numbers")

    try:
        values = list(data)
    except TypeError:
        raise TypeError("data must be an iterable of real numbers") from None

    if not values:
        raise ValueError("data must not be empty")

    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("data must contain only real numbers")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("data must contain only finite numbers")

    count = len(values)
    minimum = min(values)
    maximum = max(values)

    frequencies = Counter(values)
    highest_frequency = max(frequencies.values())
    mode = (
        None
        if highest_frequency == 1
        else min(
            value
            for value, frequency in frequencies.items()
            if frequency == highest_frequency
        )
    )

    mean = statistics.mean(values)
    median = statistics.median(values)
    std_dev = 0.0 if count == 1 else statistics.pstdev(values)

    return {
        "count": count,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": None if mode is None else round(mode, 4),
        "std_dev": round(std_dev, 4),
        "min": round(minimum, 4),
        "max": round(maximum, 4),
        "range": round(maximum - minimum, 4),
    }
