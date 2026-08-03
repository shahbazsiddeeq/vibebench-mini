from collections import Counter
from typing import Dict, Hashable, Iterable


def freq_dist(data: Iterable[Hashable]) -> Dict[Hashable, float]:
    """Return each value's relative frequency, rounded to four decimals."""
    values = list(data)
    if not values:
        raise ValueError("data must not be empty")

    total = len(values)
    return {
        value: round(count / total, 4)
        for value, count in Counter(values).items()
    }
