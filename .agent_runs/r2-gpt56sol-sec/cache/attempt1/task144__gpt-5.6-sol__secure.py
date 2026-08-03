"""Majority element implementation using the Boyer-Moore voting algorithm."""

from typing import List


def majority_element(nums: List[int]) -> int:
    """Return the strict majority element in *nums*.

    Raises:
        TypeError: If ``nums`` is not a list of integers.
        ValueError: If ``nums`` is empty or has no strict majority element.
    """
    if not isinstance(nums, list):
        raise TypeError("nums must be a list of integers")
    if not nums:
        raise ValueError("nums must not be empty")
    if any(type(value) is not int for value in nums):
        raise TypeError("nums must contain only integers")

    candidate = nums[0]
    count = 0

    for value in nums:
        if count == 0:
            candidate = value
            count = 1
        elif value == candidate:
            count += 1
        else:
            count -= 1

    occurrences = sum(1 for value in nums if value == candidate)
    if occurrences <= len(nums) // 2:
        raise ValueError("no strict majority element exists")

    return candidate
