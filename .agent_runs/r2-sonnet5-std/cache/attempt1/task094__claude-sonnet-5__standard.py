"""Descriptive Statistics module."""

from collections import Counter
import statistics


def describe(data):
    if not data:
        raise ValueError("data must not be empty")

    data = list(data)
    count = len(data)
    mean = statistics.mean(data)
    median = statistics.median(data)

    counts = Counter(data)
    max_freq = max(counts.values())
    if max_freq == 1:
        mode = None
    else:
        candidates = [val for val, freq in counts.items() if freq == max_freq]
        mode = min(candidates)

    if count > 1:
        std_dev = statistics.pstdev(data)
    else:
        std_dev = 0.0

    data_min = min(data)
    data_max = max(data)
    data_range = data_max - data_min

    def r(x):
        return round(x, 4)

    return {
        "count": count,
        "mean": r(mean),
        "median": r(median),
        "mode": mode,
        "std_dev": r(std_dev),
        "min": r(data_min),
        "max": r(data_max),
        "range": r(data_range),
    }
