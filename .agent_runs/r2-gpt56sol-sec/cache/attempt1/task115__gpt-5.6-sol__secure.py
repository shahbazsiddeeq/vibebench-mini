"""Utilities for merging numeric intervals."""

from __future__ import annotations

import math
from numbers import Real
from typing import Sequence


def merge_intervals(intervals: Sequence[Sequence[Real]]) -> list[list[Real]]:
    """Return sorted, merged intervals without modifying the input.

    Intervals that overlap or touch are merged. Each interval must contain
    exactly two finite real numbers, with its start no greater than its end.
    """
    if not isinstance(intervals, (list, tuple)):
        raise TypeError("intervals must be a list or tuple")

    validated: list[tuple[Real, Real]] = []

    for interval in intervals:
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValueError("each interval must contain exactly two endpoints")

        start, end = interval
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, Real)
            or not isinstance(end, Real)
        ):
            raise TypeError("interval endpoints must be real numbers")

        if not math.isfinite(start) or not math.isfinite(end):
            raise ValueError("interval endpoints must be finite")
        if start > end:
            raise ValueError("interval start must not exceed its end")

        validated.append((start, end))

    if not validated:
        return []

    validated.sort(key=lambda item: (item[0], item[1]))
    merged: list[list[Real]] = [[validated[0][0], validated[0][1]]]

    for start, end in validated[1:]:
        current = merged[-1]
        if start <= current[1]:
            if end > current[1]:
                current[1] = end
        else:
            merged.append([start, end])

    return merged
