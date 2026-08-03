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
    if not isinstance(nums, list):
        raise TypeError("Input 'nums' must be a list.")
    if not nums:
        raise ValueError("Input list 'nums' cannot be empty.")
    if not all(isinstance(x, int) for x in nums):
        raise TypeError("All elements in 'nums' must be integers.")

    max_so_far = -float('inf')
    current_max = 0
    start_index = 0
    end_index = 0
    current_start = 0

    # For tie-breaking:
    # When max_so_far is updated, we store the new start/end.
    # When current_max equals max_so_far, we prefer the one with smaller start,
    # then smaller end (shorter length).
    max_len = -1 # To store the length of the max_so_far subarray

    for i, num in enumerate(nums):
        # Kadane's algorithm core logic
        current_max += num

        if current_max > max_so_far:
            max_so_far = current_max
            start_index = current_start
            end_index = i
            max_len = end_index - start_index + 1
        elif current_max == max_so_far:
            # Tie-breaking: smallest start index, then smallest end index (shortest)
            current_len = i - current_start + 1
            if current_start < start_index:
                start_index = current_start
                end_index = i
                max_len = current_len
            elif current_start == start_index and current_len < max_len:
                end_index = i
                max_len = current_len

        if current_max < 0:
            # If current_max becomes negative, it's better to start a new subarray
            # from the next element.
            current_max = 0
            current_start = i + 1
            # Important: If all numbers are negative, current_max will always reset.
            # The loop above handles finding the single largest negative number.

    # Handle the case where all numbers are negative.
    # Kadane's standard algorithm might return 0 if all numbers are negative
    # and it resets current_max to 0.
    # We need to ensure we pick the single largest negative number.
    if max_so_far == 0 and all(x < 0 for x in nums):
        max_so_far = nums[0]
        start_index = 0
        end_index = 0
        for i in range(1, len(nums)):
            if nums[i] > max_so_far:
                max_so_far = nums[i]
                start_index = i
                end_index = i
            # Tie-breaking for all-negative: smallest start, then smallest end (shortest)
            # For single elements, start and end are the same, so only smallest start matters.
            elif nums[i] == max_so_far and i < start_index:
                start_index = i
                end_index = i
    elif max_so_far == -float('inf'): # This can happen if nums contains only -inf, but input validation prevents that.
        # This case should ideally not be reached with valid integer inputs.
        # If it were, it would mean all numbers are extremely small negatives.
        # We'd fall back to the largest single element.
        max_so_far = nums[0]
        start_index = 0
        end_index = 0
        for i in range(1, len(nums)):
            if nums[i] > max_so_far:
                max_so_far = nums[i]
                start_index = i
                end_index = i
            elif nums[i] == max_so_far and i < start_index:
                start_index = i
                end_index = i


    return (max_so_far, start_index, end_index)
