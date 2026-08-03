"""Utilities for searching sorted sequences."""

from typing import Any


def count_occurrences(arr: Any, target: Any) -> int:
    """Return the number of occurrences of *target* in sorted sequence *arr*.

    The sequence must support ``len(arr)`` and integer indexing. The search
    performs O(log n) element accesses.
    """
    try:
        length = len(arr)
    except (TypeError, AttributeError) as exc:
        raise TypeError("arr must be an indexable sequence") from exc

    # Find the first position whose value is not less than target.
    low, high = 0, length
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    first = low

    # Find the first position whose value is greater than target.
    low, high = first, length
    while low < high:
        mid = low + (high - low) // 2
        if target < arr[mid]:
            high = mid
        else:
            low = mid + 1

    return low - first
