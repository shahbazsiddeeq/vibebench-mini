from __future__ import annotations


def majority_element(nums: list[int]) -> int:
    """Return the strict majority element (> len(nums)//2 occurrences)."""
    if not nums:
        raise ValueError("nums must be non-empty")

    # Boyer-Moore voting to find a candidate.
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            count -= 1

    # Verification pass: the candidate must actually be a strict majority.
    occurrences = sum(1 for x in nums if x == candidate)
    if occurrences > len(nums) // 2:
        return candidate  # type: ignore[return-value]
    raise ValueError("no strict majority element exists")
