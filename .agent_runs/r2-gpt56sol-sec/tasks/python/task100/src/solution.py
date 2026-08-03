"""Frequency distribution utilities."""

from collections import Counter
from typing import Any, Dict, Iterable, Sized


def freq_dist(data: Iterable[Any]) -> Dict[Any, float]:
    """Return each value's relative frequency, rounded to four decimals.

    Raises:
        ValueError: If *data* is empty.
        TypeError: If *data* has no length or contains unhashable values.
    """
    if data is None or not isinstance(data, Sized):
        raise TypeError("data must be a sized iterable")

    total = len(data)
    if total == 0:
        raise ValueError("data must not be empty")

    try:
        counts = Counter(data)
    except TypeError as exc:
        raise TypeError("data must be iterable and contain hashable values") from exc

    return {
        value: round(count / total, 4)
        for value, count in counts.items()
    }
