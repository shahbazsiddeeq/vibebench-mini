from typing import List, Tuple


def max_subarray(nums: List[int]) -> Tuple[int, int, int]:
    """Return the maximum subarray sum and its inclusive start/end indices."""
    if not nums:
        raise ValueError("nums must be non-empty")

    current_sum = nums[0]
    current_start = 0

    best_sum = nums[0]
    best_start = 0
    best_end = 0

    for end in range(1, len(nums)):
        restart_sum = nums[end]
        extend_sum = current_sum + nums[end]

        if restart_sum > extend_sum:
            current_sum = restart_sum
            current_start = end
        else:
            current_sum = extend_sum

        if (
            current_sum > best_sum
            or (
                current_sum == best_sum
                and (current_start, end) < (best_start, best_end)
            )
        ):
            best_sum = current_sum
            best_start = current_start
            best_end = end

    return best_sum, best_start, best_end
