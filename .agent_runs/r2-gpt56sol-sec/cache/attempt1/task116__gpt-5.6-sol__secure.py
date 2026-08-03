"""Power set generation utilities."""

from itertools import combinations
from typing import Any


def power_set(elements: list[Any]) -> list[frozenset[Any]]:
    """Return all distinct subsets, ordered by size and string representation."""
    if not isinstance(elements, list):
        raise TypeError("elements must be a list")

    try:
        unique_elements = list(dict.fromkeys(elements))
    except (TypeError, ValueError) as exc:
        raise TypeError("elements must contain only hashable values") from None

    try:
        ordered_elements = sorted(unique_elements, key=str)
    except Exception:
        raise ValueError("elements must have valid string representations") from None

    result: list[frozenset[Any]] = []
    for subset_size in range(len(ordered_elements) + 1):
        for subset in combinations(ordered_elements, subset_size):
            result.append(frozenset(subset))

    return result
