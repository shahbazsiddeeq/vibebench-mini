from __future__ import annotations


def majority_element(nums: list[int]) -> int:
    """Return the strict majority element using the Boyer-Moore algorithm.

    Raises:
        ValueError: If ``nums`` is empty or has no element occurring more than
            half of the time.
    """
    if not nums:
        raise ValueError("nums must not be empty")

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

    if sum(value == candidate for value in nums) <= len(nums) // 2:
        raise ValueError("no strict majority element exists")

    return candidate
