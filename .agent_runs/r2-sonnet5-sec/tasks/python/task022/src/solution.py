"""
src/solution.py

Provides a secure, well-validated implementation of the classic
"Two Sum" problem.

two_sum(nums, target) -> (i, j)

Behavior:
    - Returns the pair of indices (i, j) with i < j such that
      nums[i] + nums[j] == target.
    - Among all valid pairs, the one with the smallest second index j
      is preferred.
    - Among all valid first indices i for that smallest j, the one
      closest to j (i.e., the largest valid i) is chosen.
    - Raises ValueError if no such pair exists or if inputs are invalid.

This implementation uses only the Python standard library and avoids
any use of eval/exec or other unsafe constructs. All inputs are
validated before processing, and internal errors are not leaked to
the caller (all failure paths raise a clean ValueError with a safe
message).
"""

from numbers import Real
from typing import Sequence, Tuple, Union


def _validate_inputs(nums: Sequence[Union[int, float]], target: Union[int, float]) -> None:
    """
    Validate that `nums` is a sequence of real numbers and `target`
    is itself a real number. Raises ValueError on any violation.
    """
    if not isinstance(nums, (list, tuple)):
        raise ValueError("Invalid input: 'nums' must be a list or tuple.")

    if isinstance(target, bool) or not isinstance(target, Real):
        raise ValueError("Invalid input: 'target' must be a numeric value.")

    for item in nums:
        if isinstance(item, bool) or not isinstance(item, Real):
            raise ValueError(
                "Invalid input: all elements of 'nums' must be numeric values."
            )


def two_sum(
    nums: Sequence[Union[int, float]], target: Union[int, float]
) -> Tuple[int, int]:
    """
    Find indices (i, j) with i < j such that nums[i] + nums[j] == target.

    Selection rule:
      - Prefer the pair with the smallest possible j (second index).
      - For that j, prefer the largest possible i (closest preceding index).

    Args:
        nums: A sequence (list or tuple) of numeric values.
        target: The target sum, a numeric value.

    Returns:
        A tuple (i, j) of indices satisfying the conditions above.

    Raises:
        ValueError: If inputs are invalid, or if no valid pair exists.
    """
    _validate_inputs(nums, target)

    # Maps a value to the most recent (largest) index at which it was seen.
    seen: dict = {}

    for j, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            i = seen[complement]
            return (i, j)
        # Update to the latest index for this value so that future
        # lookups prefer the closest preceding index.
        seen[value] = j

    raise ValueError("No two elements sum to the given target.")
