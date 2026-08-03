"""Module providing count_occurrences using binary search."""


def _lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _upper_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_occurrences(arr, target):
    """Return the number of times target appears in sorted arr.

    Uses binary search (O(log n)) to find the leftmost and rightmost
    positions of target, so it works efficiently even for objects that
    only support __len__ and __getitem__.
    """
    n = len(arr)
    if n == 0:
        return 0
    left = _lower_bound(arr, target)
    if left >= n or arr[left] != target:
        return 0
    right = _upper_bound(arr, target)
    return right - left
