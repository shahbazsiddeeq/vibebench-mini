from collections import deque
from typing import Sequence, TypeVar

T = TypeVar("T")


def sliding_max(nums: Sequence[T], k: int) -> list[T]:
    """Return the maximum value in each contiguous window of size k."""
    if k <= 0 or k > len(nums):
        raise ValueError("k must be between 1 and len(nums)")

    candidates: deque[int] = deque()
    maxima: list[T] = []

    for index, value in enumerate(nums):
        while candidates and candidates[0] <= index - k:
            candidates.popleft()

        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()

        candidates.append(index)

        if index >= k - 1:
            maxima.append(nums[candidates[0]])

    return maxima
