"""Efficient sliding-window maximum implementation."""

from collections import deque
from typing import Any, Iterable


def sliding_max(nums: Iterable[Any], k: int) -> list[Any]:
    """Return the maximum value from each consecutive window of size ``k``.

    Raises:
        TypeError: If ``k`` is not an integer or ``nums`` is not iterable.
        ValueError: If ``k`` is non-positive or exceeds the number of values.
    """
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")

    try:
        values = list(nums)
    except TypeError as exc:
        raise TypeError("nums must be iterable") from exc

    if k <= 0 or k > len(values):
        raise ValueError("k must be positive and no greater than len(nums)")

    candidates: deque[int] = deque()
    result: list[Any] = []

    for index, value in enumerate(values):
        while candidates and candidates[0] <= index - k:
            candidates.popleft()

        while candidates and values[candidates[-1]] < value:
            candidates.pop()

        candidates.append(index)

        if index >= k - 1:
            result.append(values[candidates[0]])

    return result
