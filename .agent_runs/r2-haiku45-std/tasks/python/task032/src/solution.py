def sliding_max(nums, k):
    """
    Returns a list of maximum values for each window of size k.
    
    Args:
        nums: List of integers
        k: Window size
        
    Returns:
        List of maximum values for each window
        
    Raises:
        ValueError: if k <= 0 or k > len(nums)
    """
    if k <= 0 or k > len(nums):
        raise ValueError("k must be positive and not exceed the length of nums")
    
    result = []
    for i in range(len(nums) - k + 1):
        window_max = max(nums[i:i + k])
        result.append(window_max)
    
    return result
