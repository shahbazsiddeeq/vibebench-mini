from typing import List, Sequence, TypeVar

T = TypeVar("T")


def merge_intervals(intervals: Sequence[Sequence[T]]) -> List[List[T]]:
    """Merge overlapping or touching intervals, sorted by start."""
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
    merged: List[List[T]] = [
        [sorted_intervals[0][0], sorted_intervals[0][1]]
    ]

    for interval in sorted_intervals[1:]:
        start, end = interval[0], interval[1]
        if start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])

    return merged
