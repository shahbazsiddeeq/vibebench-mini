"""
Maximum Subarray (Kadane's Algorithm) - secure implementation.

This module exposes a single function, `max_subarray`, that computes the
contiguous non-empty subarray with the maximum sum using Kadane's algorithm.

Security considerations:
- All inputs are validated before processing.
- No use of eval/exec or any dynamic code execution.
- No external I/O; the function is pure and side-effect free.
- Errors are raised with clear, non-sensitive messages (no internal state
  or stack traces are exposed to callers).
"""

from typing import List, Tuple


def _validate_nums(nums: object) -> List[int]:
    """
    Validate that `nums` is a non-empty list of integers.

    Raises:
        ValueError: if `nums` is not a list, is empty, or contains
                    non-integer elements (bool is rejected as it is not
                    considered a valid "integer" for this domain, to avoid
                    subtle type confusion bugs).
    """
    if not isinstance(nums, list):
        raise ValueError("nums must be a list of integers")

    if len(nums) == 0:
        raise ValueError("nums must be a non-empty list")

    for item in nums:
        # Explicitly reject bool since bool is a subclass of int in Python,
        # and mixing booleans into numeric computations is a common source
        # of subtle bugs / unexpected behavior.
        if isinstance(item, bool) or not isinstance(item, int):
            raise ValueError("nums must contain only integers")

    return nums


def max_subarray(nums: List[int]) -> Tuple[int, int, int]:
    """
    Find the contiguous non-empty subarray of `nums` with the largest sum.

    Args:
        nums: A non-empty list of integers.

    Returns:
        A tuple (max_sum, start, end) where start and end are inclusive
        0-based indices of the maximum sum subarray. Ties are broken by
        preferring the smallest start index, then the smallest end index
        (i.e., the shortest subarray).

    Raises:
        ValueError: if `nums` is empty or not a valid list of integers.
    """
    validated = _validate_nums(nums)
    n = len(validated)

    current_sum = validated[0]
    current_start = 0

    best_sum = validated[0]
    best_start = 0
    best_end = 0

    for i in range(1, n):
        value = validated[i]

        if current_sum < 0:
            # Restart the running subarray at this index.
            current_sum = value
            current_start = i
        else:
            current_sum += value

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = i
        elif current_sum == best_sum:
            # Tie-break: prefer smaller start, then smaller end.
            if current_start < best_start or (
                current_start == best_start and i < best_end
            ):
                best_sum = current_sum
                best_start = current_start
                best_end = i

    return (best_sum, best_start, best_end)
