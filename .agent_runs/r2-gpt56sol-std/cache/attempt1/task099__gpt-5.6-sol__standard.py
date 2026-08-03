"""Utilities for detecting statistical outliers."""

from math import sqrt
from typing import Iterable, TypeVar

T = TypeVar("T", int, float)


def find_outliers(data: Iterable[T], z_threshold: float = 2.5) -> list[T]:
    """Return values whose absolute population z-score exceeds the threshold."""
    values = list(data)
    count = len(values)

    if count < 2:
        raise ValueError("at least two data points are required")

    mean = sum(values) / count
    variance = sum((value - mean) ** 2 for value in values) / count

    if variance == 0:
        return []

    standard_deviation = sqrt(variance)
    return [
        value
        for value in values
        if abs((value - mean) / standard_deviation) > z_threshold
    ]
