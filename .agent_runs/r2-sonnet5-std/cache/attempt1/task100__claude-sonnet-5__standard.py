"""Frequency Distribution module."""
from collections import Counter


def freq_dist(data):
    """Return {value: relative_frequency} rounded to 4 decimal places.

    Raises ValueError if data is empty.
    """
    if not data:
        raise ValueError("data must not be empty")

    counts = Counter(data)
    n = len(data)
    return {value: round(count / n, 4) for value, count in counts.items()}
