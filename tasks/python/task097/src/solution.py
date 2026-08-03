import math


def z_scores(data: list[float]) -> list[float]:
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance)
    if std == 0:
        raise ValueError("Standard deviation is zero")
    return [(x - mean) / std for x in data]
