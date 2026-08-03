from bisect import bisect_right
from operator import index
from typing import Iterable


def histogram(
    data: Iterable[float], bins: int
) -> list[tuple[float, float, int]]:
    """Return equal-width histogram bins spanning the range of *data*."""
    try:
        bin_count = index(bins)
    except TypeError as exc:
        raise ValueError("bins must be a positive integer") from exc

    if bin_count < 1:
        raise ValueError("bins must be at least 1")

    values = list(data)
    if not values:
        raise ValueError("data must not be empty")

    minimum = float(min(values))
    maximum = float(max(values))

    if minimum == maximum:
        return [(minimum, maximum, len(values))]

    width = (maximum - minimum) / bin_count
    edges = [minimum + width * i for i in range(bin_count)]
    edges.append(maximum)

    counts = [0] * bin_count
    for value in values:
        position = bisect_right(edges, float(value)) - 1
        if position == bin_count:
            position = bin_count - 1
        counts[position] += 1

    return [
        (edges[i], edges[i + 1], counts[i])
        for i in range(bin_count)
    ]
