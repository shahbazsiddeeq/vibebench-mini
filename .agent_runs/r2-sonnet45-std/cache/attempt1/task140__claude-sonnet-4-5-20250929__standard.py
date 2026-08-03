def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    if not nums:
        raise ValueError("Input list cannot be empty")
    
    # Initialize with the first element
    max_sum = nums[0]
    max_start = 0
    max_end = 0
    
    # Current subarray tracking
    current_sum = nums[0]
    current_start = 0
    
    for i in range(1, len(nums)):
        # If adding current element is worse than starting fresh from current element
        if nums[i] > current_sum + nums[i]:
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
            # Tie-breaking: prefer smallest start, then smallest end (shortest)
            if current_start < max_start or (current_start == max_start and i < max_end):
                max_start = current_start
                max_end = i
    
    return (max_sum, max_start, max_end)
