"""Percentile calculation using linear interpolation."""

from __future__ import annotations

import math
from collections.abc import Iterable
from numbers import Real


def percentile(data: Iterable[Real], p: Real) -> float:
    """Return the ``p``th percentile of *data* using linear interpolation.

    The percentile rank must be between 0 and 100, inclusive. Data is sorted
    before calculation, and the interpolation position is based on ``n - 1``.

    Raises:
        TypeError: If inputs are not valid numeric values.
        ValueError: If data is empty, contains non-finite values, or the
            percentile rank is outside the inclusive range 0 to 100.
    """
    if isinstance(p, bool) or not isinstance(p, Real):
        raise TypeError("p must be a real number")

    try:
        rank = float(p)
    except (TypeError, ValueError, OverflowError) as exc:
        raise TypeError("p must be a real number") from exc

    if not math.isfinite(rank) or not 0.0 <= rank <= 100.0:
        raise ValueError("p must be between 0 and 100")

    if isinstance(data, (str, bytes, bytearray)) or not isinstance(data, Iterable):
        raise TypeError("data must be an iterable of real numbers")

    values: list[float] = []
    for value in data:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("data must contain only real numbers")
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise TypeError("data must contain only real numbers") from exc
        if not math.isfinite(number):
            raise ValueError("data must contain only finite values")
        values.append(number)

    if not values:
        raise ValueError("data must not be empty")

    values.sort()

    position = (len(values) - 1) * rank / 100.0
    lower_index = math.floor(position)
    upper_index = math.ceil(position)

    if lower_index == upper_index:
        return values[lower_index]

    fraction = position - lower_index
    lower = values[lower_index]
    upper = values[upper_index]
    return lower + (upper - lower) * fraction
