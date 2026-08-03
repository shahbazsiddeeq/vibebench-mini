def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """
    Find the contiguous non-empty subarray with the largest sum.
    
    Returns (max_sum, start, end) where start and end are inclusive 0-based indices.
    Handles negatives and all-negative arrays.
    Tie-break: smallest start index, then smallest end index (shortest).
    
    Raises ValueError if nums is empty.
    """
    # Input validation
    if not isinstance(nums, list):
        raise ValueError("Input must be a list")
    
    if len(nums) == 0:
        raise ValueError("Input list cannot be empty")
    
    # Validate all elements are integers
    for item in nums:
        if not isinstance(item, int):
            raise ValueError("All elements must be integers")
    
    # Initialize tracking variables
    max_sum = nums[0]
    max_start = 0
    max_end = 0
    
    current_sum = nums[0]
    current_start = 0
    
    # Kadane's algorithm with tie-breaking logic
    for i in range(1, len(nums)):
        # Decide whether to extend current subarray or start fresh
        # Start fresh if current_sum is negative (to get smallest start index on tie)
        if current_sum < 0:
            current_sum = nums[i]
            current_start = i
        else:
            current_sum += nums[i]
        
        # Update max if we found a better sum, or same sum with better indices
        if current_sum > max_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = i
        elif current_sum == max_sum:
            # Tie-break: prefer smallest start, then smallest end (shortest)
            if current_start < max_start:
                max_start = current_start
                max_end = i
            elif current_start == max_start and i < max_end:
                max_end = i
    
    return (max_sum, max_start, max_end)
