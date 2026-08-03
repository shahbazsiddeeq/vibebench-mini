"""
Frequency Distribution module.

Provides freq_dist(data) which computes the relative frequency of each
distinct value in an iterable, rounded to 4 decimal places.

This module avoids eval/exec, performs no I/O, and validates input
defensively without leaking internal error details.
"""

from collections.abc import Iterable, Hashable
from typing import Any, Dict


def freq_dist(data: Iterable[Any]) -> Dict[Any, float]:
    """
    Compute the relative frequency distribution of values in `data`.

    Args:
        data: An iterable (e.g., list, tuple) of hashable values.

    Returns:
        A dict mapping each distinct value to its relative frequency
        (count of occurrences divided by total length), rounded to
        4 decimal places.

    Raises:
        ValueError: If `data` is not a valid non-empty iterable of
            hashable values.
    """
    # Validate that data is an iterable (but not something exotic like
    # a generator we can't safely materialize twice); we materialize
    # into a list defensively.
    if data is None:
        raise ValueError("data must be a non-empty iterable")

    if isinstance(data, (str, bytes)):
        # Treat strings/bytes as sequences of characters/bytes,
        # which is well-defined and safe.
        pass
    elif not isinstance(data, Iterable):
        raise ValueError("data must be an iterable")

    try:
        items = list(data)
    except TypeError as exc:
        raise ValueError("data must be a non-empty iterable") from exc

    if len(items) == 0:
        raise ValueError("data must not be empty")

    counts: Dict[Any, int] = {}
    for item in items:
        if not isinstance(item, Hashable):
            raise ValueError("all elements of data must be hashable")
        counts[item] = counts.get(item, 0) + 1

    total = len(items)
    result: Dict[Any, float] = {}
    for value, count in counts.items():
        result[value] = round(count / total, 4)

    return result
