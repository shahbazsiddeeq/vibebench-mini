"""
src/solution.py

Sliding Window Maximum implementation.

This module provides `sliding_max(nums, k)`, which returns the maximum
value of each contiguous window of size `k` in the input sequence `nums`.

Security / robustness considerations:
- No use of eval/exec or any dynamic code execution.
- No I/O operations; the function operates purely on in-memory data.
- Strict input validation: type checks on `nums` and `k`, with clear,
  non-leaky error messages (no internal state or stack traces exposed).
- Defensive copying: the input list is not mutated.
- No external/third-party dependencies; standard library only
  (`collections.deque` for O(n) sliding window maximum).
"""

from collections import deque
from numbers import Integral
from typing import List, Sequence, Union


Number = Union[int, float]


def sliding_max(nums: Sequence[Number], k: int) -> List[Number]:
    """
    Return a list of the maximum values for each sliding window of size k.

    Args:
        nums: A sequence (e.g., list or tuple) of numbers.
        k: The window size. Must be a positive integer not exceeding
           the length of nums.

    Returns:
        A list of maximums for each window of size k, in order.

    Raises:
        ValueError: If k <= 0, k > len(nums), nums is not a valid
                    sequence of numbers, or k is not an integer.
    """
    # Validate nums: must be a list/tuple (sequence) of numbers, not str/bytes.
    if isinstance(nums, (str, bytes, bytearray)):
        raise ValueError("nums must be a sequence of numbers, not a string/bytes type")

    if not isinstance(nums, Sequence):
        raise ValueError("nums must be a sequence (list or tuple) of numbers")

    # Make a defensive local copy as a list to avoid mutating caller's data
    # and to ensure consistent indexing behavior.
    try:
        nums_list = list(nums)
    except TypeError as exc:
        raise ValueError("nums could not be converted to a list") from exc

    for item in nums_list:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError("nums must contain only numeric (int or float) values")

    # Validate k: must be an integer type (bool excluded), positive, and <= len(nums)
    if isinstance(k, bool) or not isinstance(k, Integral):
        raise ValueError("k must be an integer")

    k = int(k)

    n = len(nums_list)

    if k <= 0:
        raise ValueError("k must be a positive integer")

    if k > n:
        raise ValueError("k must not exceed the length of nums")

    # Sliding window maximum using a monotonic deque of indices.
    result: List[Number] = []
    dq: deque = deque()  # will store indices, values decreasing

    for i, value in enumerate(nums_list):
        # Remove indices that are out of the current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices whose values are less than the current value,
        # since they can never be the maximum while current value is in window
        while dq and nums_list[dq[-1]] < value:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums_list[dq[0]])

    return result
