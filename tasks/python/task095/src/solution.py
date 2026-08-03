from __future__ import annotations


def percentile(data: list[float], p: float) -> float:
    if not data:
        raise ValueError("data must not be empty")
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 1:
        return float(sorted_data[0])
    index = (p / 100) * (n - 1)
    lo = int(index)
    hi = lo + 1
    if hi >= n:
        return float(sorted_data[-1])
    frac = index - lo
    return sorted_data[lo] + frac * (sorted_data[hi] - sorted_data[lo])
