from __future__ import annotations

import bisect


def count_occurrences(arr: list[int], target: int) -> int:
    left = bisect.bisect_left(arr, target)
    right = bisect.bisect_right(arr, target)
    return right - left
