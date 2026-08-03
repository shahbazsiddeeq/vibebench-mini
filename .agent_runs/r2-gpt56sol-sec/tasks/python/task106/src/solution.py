"""Equal-width histogram binning."""

from bisect import bisect_right
from math import isfinite
from numbers import Integral, Real
from typing import Iterable


def histogram(
    data: Iterable[Real], bins: int
) -> list[tuple[float, float, int]]:
    """Return equal-width histogram bins spanning the supplied data."""
    if isinstance(bins, bool) or not isinstance(bins, Integral) or bins < 1:
        raise ValueError("bins must be a positive integer")

    if data is None:
        raise ValueError("data must not be empty")

    try:
        raw_values = list(data)
    except TypeError as exc:
        raise ValueError("data must be an iterable of real numbers") from exc

    if not raw_values:
        raise ValueError("data must not be empty")

    values: list[float] = []
    for value in raw_values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError("data must contain only real numbers")
        try:
            converted = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("data contains an invalid numeric value") from exc
        if not isfinite(converted):
            raise ValueError("data values must be finite")
        values.append(converted)

    minimum = min(values)
    maximum = max(values)

    if minimum == maximum:
        return [(minimum, maximum, len(values))]

    bin_count = int(bins)
    span = maximum - minimum
    edges = [
        minimum + span * index / bin_count
        for index in range(bin_count + 1)
    ]
    edges[0] = minimum
    edges[-1] = maximum

    interior_edges = edges[1:-1]
    counts = [0] * bin_count
    for value in values:
        index = bisect_right(interior_edges, value)
        counts[index] += 1

    return [
        (edges[index], edges[index + 1], counts[index])
        for index in range(bin_count)
    ]
