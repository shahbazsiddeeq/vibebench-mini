from collections import Counter
from math import fsum
from typing import Iterable, Optional, Union

Number = Union[int, float]


def describe(data: Iterable[Number]) -> dict:
    values = list(data)
    if not values:
        raise ValueError("data must not be empty")

    count = len(values)
    ordered = sorted(values)

    mean = fsum(values) / count

    midpoint = count // 2
    if count % 2:
        median = ordered[midpoint]
    else:
        median = (ordered[midpoint - 1] + ordered[midpoint]) / 2

    frequencies = Counter(values)
    highest_frequency = max(frequencies.values())
    mode: Optional[Number]
    if highest_frequency == 1:
        mode = None
    else:
        mode = min(
            value
            for value, frequency in frequencies.items()
            if frequency == highest_frequency
        )

    if count == 1:
        std_dev = 0.0
    else:
        variance = fsum((value - mean) ** 2 for value in values) / count
        std_dev = variance ** 0.5

    minimum = min(values)
    maximum = max(values)

    return {
        "count": count,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": None if mode is None else round(mode, 4),
        "std_dev": round(std_dev, 4),
        "min": round(minimum, 4),
        "max": round(maximum, 4),
        "range": round(maximum - minimum, 4),
    }
