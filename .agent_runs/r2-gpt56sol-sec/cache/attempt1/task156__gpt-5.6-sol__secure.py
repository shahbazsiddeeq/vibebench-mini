"""Weighted average calculation utilities."""

from math import isfinite
from typing import List, Union

Number = Union[int, float]


def weighted_average(values: List[Number], weights: List[Number]) -> float:
    """Return the weighted arithmetic mean rounded to six decimal places."""
    if not isinstance(values, list) or not isinstance(weights, list):
        raise TypeError("values and weights must be lists")

    if not values:
        raise ValueError("values must not be empty")
    if not weights:
        raise ValueError("weights must not be empty")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")

    for item in values:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise TypeError("values must contain only numbers")
        if isinstance(item, float) and not isfinite(item):
            raise ValueError("values must contain only finite numbers")

    for item in weights:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise TypeError("weights must contain only numbers")
        if isinstance(item, float) and not isfinite(item):
            raise ValueError("weights must contain only finite numbers")

    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("sum of weights must not be zero")

    weighted_sum = sum(value * weight for value, weight in zip(values, weights))
    return float(round(weighted_sum / total_weight, 6))
