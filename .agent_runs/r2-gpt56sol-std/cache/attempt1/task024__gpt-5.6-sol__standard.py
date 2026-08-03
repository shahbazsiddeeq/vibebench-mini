"""Utilities for counting values in sorted sequences."""


def count_occurrences(arr, target):
    """Return the number of occurrences of *target* in sorted sequence *arr*."""

    def lower_bound(value):
        left, right = 0, len(arr)
        while left < right:
            middle = (left + right) // 2
            if arr[middle] < value:
                left = middle + 1
            else:
                right = middle
        return left

    first = lower_bound(target)

    left, right = first, len(arr)
    while left < right:
        middle = (left + right) // 2
        if arr[middle] <= target:
            left = middle + 1
        else:
            right = middle

    return left - first
