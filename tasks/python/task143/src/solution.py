from __future__ import annotations

import random


def kth_largest(nums: list[int], k: int) -> int:
    """Return the k-th largest element (k=1 is the maximum) via quickselect."""
    n = len(nums)
    if n == 0:
        raise ValueError("nums must be non-empty")
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValueError("k must be an int")
    if k < 1 or k > n:
        raise ValueError("k must be in range 1..len(nums)")

    # k-th largest == (k-1) index when sorted descending == (n-k) index ascending.
    target = n - k
    arr = list(nums)
    lo, hi = 0, n - 1

    while True:
        if lo == hi:
            return arr[lo]
        pivot_index = random.randint(lo, hi)
        pivot_index = _partition(arr, lo, hi, pivot_index)
        if pivot_index == target:
            return arr[pivot_index]
        elif pivot_index < target:
            lo = pivot_index + 1
        else:
            hi = pivot_index - 1


def _partition(arr: list[int], lo: int, hi: int, pivot_index: int) -> int:
    pivot_value = arr[pivot_index]
    arr[pivot_index], arr[hi] = arr[hi], arr[pivot_index]
    store = lo
    for i in range(lo, hi):
        if arr[i] < pivot_value:
            arr[i], arr[store] = arr[store], arr[i]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    return store
