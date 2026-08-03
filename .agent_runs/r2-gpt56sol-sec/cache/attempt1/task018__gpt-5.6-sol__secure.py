"""Iterative binary search implementation."""

from typing import Any, Sequence


def binary_search(arr: Sequence[Any], target: Any) -> int:
    """Return the index of *target* in sorted *arr*, or -1 if absent."""
    low = 0
    high = len(arr) - 1

    while low <= high:
        middle = low + (high - low) // 2
        value = arr[middle]

        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1
