"""
src/solution.py

A secure, self-contained module implementing an interval-merging utility.

Function:
    merge_intervals(intervals): merges overlapping or touching [start, end]
    pairs and returns the merged, non-overlapping intervals sorted by start.
"""

from numbers import Real
from typing import List, Sequence, Union

Number = Union[int, float]


def _validate_interval(interval, index: int) -> None:
    """
    Validate a single interval entry without leaking internal details
    beyond a clear, safe error message.
    """
    if isinstance(interval, (str, bytes)):
        raise TypeError(f"Interval at index {index} must be a sequence of two numbers, not a string/bytes.")

    if not isinstance(interval, Sequence):
        raise TypeError(f"Interval at index {index} must be a sequence (e.g., list or tuple).")

    if len(interval) != 2:
        raise ValueError(f"Interval at index {index} must contain exactly two elements [start, end].")

    start, end = interval[0], interval[1]

    for value, label in ((start, "start"), (end, "end")):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"Interval at index {index}: '{label}' must be a real number.")

    if start > end:
        raise ValueError(f"Interval at index {index}: start ({start!r}) must not be greater than end ({end!r}).")


def merge_intervals(intervals: List[Sequence[Number]]) -> List[List[Number]]:
    """
    Merge overlapping or touching intervals.

    Args:
        intervals: A list of [start, end] pairs (lists or tuples of two
            real numbers, with start <= end). The list may be empty and
            need not be sorted.

    Returns:
        A new list of [start, end] lists representing the merged,
        non-overlapping intervals, sorted by start ascending.

    Raises:
        TypeError: If `intervals` is not a list/sequence, or if an
            individual interval is malformed (not a two-element sequence
            of real numbers).
        ValueError: If an interval has start > end, or does not contain
            exactly two elements.
    """
    if isinstance(intervals, (str, bytes)):
        raise TypeError("intervals must be a list of [start, end] pairs, not a string/bytes.")

    if not isinstance(intervals, Sequence):
        raise TypeError("intervals must be a list (or sequence) of [start, end] pairs.")

    if len(intervals) == 0:
        return []

    # Validate and normalize into plain (start, end) tuples of numbers.
    normalized = []
    for idx, interval in enumerate(intervals):
        _validate_interval(interval, idx)
        start, end = interval[0], interval[1]
        normalized.append((start, end))

    # Sort by start, then end, ascending.
    normalized.sort(key=lambda pair: (pair[0], pair[1]))

    merged: List[List[Number]] = []
    for start, end in normalized:
        if merged and start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])

    return merged
