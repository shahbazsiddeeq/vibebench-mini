"""Outlier detection based on population z-score."""

import math


def find_outliers(data, z_threshold=2.5):
    n = len(data)
    if n < 2:
        raise ValueError("data must contain at least 2 elements")

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std = math.sqrt(variance)

    if std == 0:
        return []

    return [x for x in data if abs((x - mean) / std) > z_threshold]
