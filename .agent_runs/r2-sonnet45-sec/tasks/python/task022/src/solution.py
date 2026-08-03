def two_sum(nums, target):
    """
    Find two indices (i, j) with i < j such that nums[i] + nums[j] == target.
    
    When multiple valid pairs exist, return the pair with the smallest second 
    index j. Among indices that could pair with that j, use the largest such i.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        Tuple (i, j) with i < j where nums[i] + nums[j] == target
        
    Raises:
        ValueError: If no valid pair exists
    """
    # Input validation
    if not isinstance(nums, (list, tuple)):
        raise ValueError("nums must be a list or tuple")
    if not isinstance(target, (int, float)):
        raise ValueError("target must be a number")
    if len(nums) < 2:
        raise ValueError("nums must contain at least 2 elements")
    
    # Validate all elements are numbers
    for num in nums:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements in nums must be numbers")
    
    # Iterate through potential j values (second index) from left to right
    for j in range(1, len(nums)):
        complement = target - nums[j]
        
        # Look for the largest i < j where nums[i] == complement
        # Search backwards from j-1 to 0 to find the largest valid i
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                return (i, j)
    
    # No valid pair found
    raise ValueError("No two sum solution exists")
