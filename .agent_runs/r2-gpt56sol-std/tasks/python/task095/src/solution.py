"""Percentile calculation using linear interpolation."""

from math import floor
from typing import Iterable


def percentile(data: Iterable[float], p: float) -> float:
    """Return the pth percentile of data using linear interpolation.

    Args:
        data: An iterable of numeric values.
        p: The desired percentile, from 0 through 100 inclusive.

    Raises:
        ValueError: If data is empty or p is outside the valid range.
    """
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")

    values = sorted(data)
    if not values:
        raise ValueError("data must not be empty")

    position = (len(values) - 1) * (p / 100.0)
    lower_index = floor(position)
    upper_index = min(lower_index + 1, len(values) - 1)
    fraction = position - lower_index

    lower = values[lower_index]
    upper = values[upper_index]
    return float(lower + (upper - lower) * fraction)
