"""Maximum subarray implementation."""

from typing import Final


def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """Return the maximum subarray sum and its inclusive start/end indices.

    Ties are resolved by choosing the smallest start index, followed by the
    smallest end index.

    Raises:
        TypeError: If ``nums`` is not a list of integers.
        ValueError: If ``nums`` is empty.
    """
    if not isinstance(nums, list):
        raise TypeError("nums must be a list of integers")
    if not nums:
        raise ValueError("nums must not be empty")
    if any(type(value) is not int for value in nums):
        raise TypeError("nums must contain only integers")

    current_sum: int = nums[0]
    current_start: int = 0

    best_sum: int = nums[0]
    best_start: int = 0
    best_end: int = 0

    for end in range(1, len(nums)):
        value: Final[int] = nums[end]
        extended_sum = current_sum + value

        # On equal sums, extending preserves the smaller start index.
        if extended_sum >= value:
            current_sum = extended_sum
        else:
            current_sum = value
            current_start = end

        if (
            current_sum > best_sum
            or (
                current_sum == best_sum
                and (
                    current_start < best_start
                    or (current_start == best_start and end < best_end)
                )
            )
        ):
            best_sum = current_sum
            best_start = current_start
            best_end = end

    return best_sum, best_start, best_end
