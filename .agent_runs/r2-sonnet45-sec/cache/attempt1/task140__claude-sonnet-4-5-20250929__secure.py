def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """
    Find the contiguous non-empty subarray with the largest sum.
    
    Args:
        nums: List of integers
        
    Returns:
        Tuple of (max_sum, start_index, end_index) where indices are inclusive
        
    Raises:
        ValueError: If nums is empty
    """
    # Validate input
    if not isinstance(nums, list):
        raise ValueError("Input must be a list")
    
    if len(nums) == 0:
        raise ValueError("Input list cannot be empty")
    
    # Validate all elements are integers
    for item in nums:
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            raise ValueError("All elements must be numeric")
    
    # Initialize with the first element
    max_sum = nums[0]
    max_start = 0
    max_end = 0
    
    # Current subarray tracking
    current_sum = nums[0]
    current_start = 0
    
    # Iterate through the rest of the array
    for i in range(1, len(nums)):
        # Decide whether to extend current subarray or start new one
        if current_sum + nums[i] > nums[i]:
            # Extend current subarray
            current_sum += nums[i]
        else:
            # Start new subarray from current position
            current_sum = nums[i]
            current_start = i
        
        # Update maximum if we found a better subarray
        # Tie-breaking: prefer smaller start, then smaller end (shorter)
        if (current_sum > max_sum or 
            (current_sum == max_sum and current_start < max_start) or
            (current_sum == max_sum and current_start == max_start and i < max_end)):
            max_sum = current_sum
            max_start = current_start
            max_end = i
    
    return (max_sum, max_start, max_end)
