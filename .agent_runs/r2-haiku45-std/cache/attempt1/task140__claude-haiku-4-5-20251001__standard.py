def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """
    Finds the contiguous non-empty subarray with the largest sum.
    
    Returns (max_sum, start, end) where start and end are inclusive 0-based indices.
    Handles negatives and all-negative arrays.
    Tie-break: smallest start index, then smallest end index (shortest).
    
    Raises ValueError if nums is empty.
    """
    if not nums:
        raise ValueError("nums cannot be empty")
    
    max_sum = nums[0]
    max_start = 0
    max_end = 0
    
    current_sum = nums[0]
    current_start = 0
    
    for i in range(1, len(nums)):
        # If current_sum is negative, start fresh from current element
        if current_sum < 0:
            current_sum = nums[i]
            current_start = i
        else:
            current_sum += nums[i]
        
        # Update max if we found a better sum, or same sum with better tie-break
        if current_sum > max_sum or (current_sum == max_sum and current_start < max_start):
            max_sum = current_sum
            max_start = current_start
            max_end = i
        elif current_sum == max_sum and current_start == max_start and i < max_end:
            # Same sum, same start, but shorter subarray
            max_end = i
    
    return (max_sum, max_start, max_end)
