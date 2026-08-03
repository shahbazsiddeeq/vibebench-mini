"""Quicksort implementation without using Python's built-in sorting tools."""

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def quicksort(lst: Iterable[T]) -> List[T]:
    """Return a new list containing the elements of *lst* in sorted order."""
    result = list(lst)

    if len(result) < 2:
        return result

    ranges = [(0, len(result) - 1)]

    while ranges:
        low, high = ranges.pop()
        pivot = result[(low + high) // 2]

        # Three-way partition into values below, equal to, and above the pivot.
        left = current = low
        right = high

        while current <= right:
            if result[current] < pivot:
                result[left], result[current] = result[current], result[left]
                left += 1
                current += 1
            elif pivot < result[current]:
                result[current], result[right] = result[right], result[current]
                right -= 1
            else:
                current += 1

        lower_range = (low, left - 1)
        upper_range = (right + 1, high)

        # Add the larger range first so the smaller one is processed next,
        # keeping the explicit stack relatively small.
        lower_size = lower_range[1] - lower_range[0] + 1
        upper_size = upper_range[1] - upper_range[0] + 1

        if lower_size > upper_size:
            if lower_size > 1:
                ranges.append(lower_range)
            if upper_size > 1:
                ranges.append(upper_range)
        else:
            if upper_size > 1:
                ranges.append(upper_range)
            if lower_size > 1:
                ranges.append(lower_range)

    return result
