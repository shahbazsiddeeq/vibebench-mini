"""Quickselect implementation for finding the k-th largest integer."""

from __future__ import annotations

import secrets


def kth_largest(nums: list[int], k: int) -> int:
    """Return the k-th largest value in *nums*, counting duplicates.

    Args:
        nums: A non-empty list of integers.
        k: One-based rank, where 1 identifies the largest value.

    Raises:
        TypeError: If the arguments have invalid types.
        ValueError: If ``nums`` is empty or ``k`` is outside its valid range.
    """
    if not isinstance(nums, list):
        raise TypeError("nums must be a list of integers")
    if any(type(value) is not int for value in nums):
        raise TypeError("nums must contain only integers")
    if type(k) is not int:
        raise TypeError("k must be an integer")
    if not nums:
        raise ValueError("nums must not be empty")
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")

    values = nums.copy()
    target = k - 1
    left = 0
    right = len(values) - 1

    while left <= right:
        pivot = values[left + secrets.randbelow(right - left + 1)]

        # Three-way partition in descending order:
        # [left, greater) > pivot
        # [greater, scan) == pivot
        # (lesser, right] < pivot
        greater = left
        scan = left
        lesser = right

        while scan <= lesser:
            if values[scan] > pivot:
                values[greater], values[scan] = values[scan], values[greater]
                greater += 1
                scan += 1
            elif values[scan] < pivot:
                values[scan], values[lesser] = values[lesser], values[scan]
                lesser -= 1
            else:
                scan += 1

        if target < greater:
            right = greater - 1
        elif target > lesser:
            left = lesser + 1
        else:
            return pivot

    raise RuntimeError("selection failed")
