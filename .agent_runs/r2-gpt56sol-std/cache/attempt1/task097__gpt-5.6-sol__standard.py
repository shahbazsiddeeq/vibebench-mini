"""Z-score normalization utilities."""

from math import fsum, sqrt
from typing import Iterable


def z_scores(data: Iterable[float]) -> list[float]:
    """Return population z-scores for the values in *data*.

    Raises:
        ValueError: If fewer than two values are supplied or all values are equal.
    """
    values = list(data)
    if len(values) < 2:
        raise ValueError("at least two data points are required")

    mean = fsum(values) / len(values)
    variance = fsum((value - mean) ** 2 for value in values) / len(values)
    std = sqrt(variance)

    if std == 0:
        raise ValueError("standard deviation must be nonzero")

    return [(value - mean) / std for value in values]
