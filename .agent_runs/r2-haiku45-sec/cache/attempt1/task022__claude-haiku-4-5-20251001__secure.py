def two_sum(nums, target):
    """
    Returns a tuple (i, j) with i < j such that nums[i] + nums[j] == target.
    
    When more than one valid pair exists:
    - Return the pair with the smallest second index j
    - Among indices that could pair with that j, use the largest such i
    
    Raises ValueError if no pair sums to target.
    """
    # Input validation
    if not isinstance(nums, (list, tuple)):
        raise ValueError("nums must be a list or tuple")
    if not isinstance(target, (int, float)):
        raise ValueError("target must be a number")
    
    if len(nums) < 2:
        raise ValueError("nums must have at least 2 elements")
    
    # Validate all elements are numbers
    for num in nums:
        if not isinstance(num, (int, float)):
            raise ValueError("all elements in nums must be numbers")
    
    # Strategy: iterate through j from left to right (to get smallest j first)
    # For each j, find the largest i < j such that nums[i] + nums[j] == target
    
    for j in range(1, len(nums)):
        complement = target - nums[j]
        
        # Search backwards from j-1 to find the largest i that matches
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                return (i, j)
    
    # No valid pair found
    raise ValueError("No pair found that sums to target")
