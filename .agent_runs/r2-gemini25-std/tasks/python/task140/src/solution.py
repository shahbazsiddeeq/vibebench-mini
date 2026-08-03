def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """
    Finds the contiguous non-empty subarray of nums with the largest sum.

    Args:
        nums: A list of integers.

    Returns:
        A tuple (max_sum, start, end) where max_sum is the largest sum,
        and start and end are inclusive 0-based indices of the subarray.

    Raises:
        ValueError: If nums is empty.
    """
    if not nums:
        raise ValueError("Input list 'nums' cannot be empty.")

    max_so_far = float('-inf')
    current_max = 0
    start_index = 0
    end_index = 0
    current_start = 0

    # Variables for tie-breaking
    best_start = 0
    best_end = 0

    for i, num in enumerate(nums):
        current_max += num

        if current_max > max_so_far:
            max_so_far = current_max
            best_start = current_start
            best_end = i
        elif current_max == max_so_far:
            # Tie-breaking: smallest start index, then smallest end index (shortest)
            if current_start < best_start:
                best_start = current_start
                best_end = i
            elif current_start == best_start and i < best_end:
                best_end = i

        if current_max < 0:
            current_max = 0
            current_start = i + 1

    # Handle the case where all numbers are negative
    # In this scenario, Kadane's algorithm above would reset current_max to 0
    # and current_start to i+1, potentially missing the single largest negative number.
    # We need to re-evaluate if max_so_far is still -inf (meaning all sums were negative)
    # or if the best subarray found was a positive sum.
    # If all numbers are negative, the max_so_far will be the largest single negative number.
    # The loop above correctly identifies this if current_max is updated before it goes negative.
    # However, the tie-breaking logic for all-negative arrays needs careful consideration.

    # A simpler approach for all-negative arrays:
    # If max_so_far is still negative after the loop, it means all subarrays had negative sums.
    # In this case, the maximum subarray is the single element with the largest value.
    if max_so_far < 0:
        max_so_far = nums[0]
        best_start = 0
        best_end = 0
        for i in range(1, len(nums)):
            if nums[i] > max_so_far:
                max_so_far = nums[i]
                best_start = i
                best_end = i
            # Tie-breaking for all-negative: smallest start, then smallest end (shortest)
            # If nums[i] == max_so_far, and i < best_start, update.
            # This is implicitly handled by picking the first occurrence if values are equal.
            # For single elements, start == end, so shortest is not applicable.
            # Smallest start index is the primary tie-breaker.
            elif nums[i] == max_so_far and i < best_start:
                best_start = i
                best_end = i

    return (max_so_far, best_start, best_end)
