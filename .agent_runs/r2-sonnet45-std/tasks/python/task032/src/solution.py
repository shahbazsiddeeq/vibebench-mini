def sliding_max(nums, k):
    """
    Returns a list of maximum values for each window of size k.
    
    Args:
        nums: List of numbers
        k: Window size
        
    Returns:
        List of maximum values for each sliding window
        
    Raises:
        ValueError: If k <= 0 or k > len(nums)
    """
    if k <= 0 or k > len(nums):
        raise ValueError("k must be positive and not greater than length of nums")
    
    result = []
    
    # Iterate through all possible windows
    for i in range(len(nums) - k + 1):
        # Get the window from index i to i+k
        window = nums[i:i+k]
        # Find and append the maximum value in this window
        result.append(max(window))
    
    return result
