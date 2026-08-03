from __future__ import annotations


def moving_average(data: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(data):
        raise ValueError("window must not exceed len(data)")
    return [sum(data[i : i + window]) / window for i in range(len(data) - window + 1)]
