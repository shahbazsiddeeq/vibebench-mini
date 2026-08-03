def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """
    Find the contiguous non-empty subarray of nums with the largest sum.

    Returns a tuple (max_sum, start, end) where start and end are inclusive
    0-based indices. Handles negative numbers and all-negative arrays
    (the max may be a single element). When several subarrays share the
    maximum sum, ties are broken by smallest start index, then smallest
    end index (shortest subarray).

    Raises ValueError if nums is empty.
    """
    if not nums:
        raise ValueError("nums must not be empty")

    n = len(nums)

    cur_sum = nums[0]
    cur_start = 0

    best_sum = cur_sum
    best_start = 0
    best_end = 0

    for i in range(1, n):
        if cur_sum >= 0:
            cur_sum += nums[i]
            # cur_start stays the same
        else:
            cur_sum = nums[i]
            cur_start = i

        if cur_sum > best_sum:
            best_sum = cur_sum
            best_start = cur_start
            best_end = i
        elif cur_sum == best_sum:
            if cur_start < best_start or (cur_start == best_start and i < best_end):
                best_start = cur_start
                best_end = i

    return best_sum, best_start, best_end
