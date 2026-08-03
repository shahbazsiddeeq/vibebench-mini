from __future__ import annotations

import statistics
from collections import Counter


def describe(data: list[float]) -> dict:
    if not data:
        raise ValueError("data must not be empty")
    n = len(data)
    mean = statistics.mean(data)
    median = statistics.median(data)
    counts = Counter(data)
    max_count = max(counts.values())
    if max_count == 1:
        mode = None
    else:
        mode = min(v for v, c in counts.items() if c == max_count)
    std_dev = statistics.pstdev(data) if n > 1 else 0.0
    return {
        "count": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": round(mode, 4) if isinstance(mode, float) else mode,
        "std_dev": round(std_dev, 4),
        "min": round(min(data), 4),
        "max": round(max(data), 4),
        "range": round(max(data) - min(data), 4),
    }
