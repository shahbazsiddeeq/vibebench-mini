import math


def find_outliers(data: list[float], z_threshold: float = 2.5) -> list[float]:
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance)
    if std == 0:
        return []
    return [x for x in data if abs((x - mean) / std) > z_threshold]
