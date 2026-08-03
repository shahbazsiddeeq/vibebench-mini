def two_sum(nums, target):
    """
    Returns a tuple (i, j) with i < j such that nums[i] + nums[j] == target.
    
    When more than one valid pair exists, return the pair with the smallest 
    second index j; among indices that could pair with that j, use the largest 
    such i (that is, the index closest before j).
    
    Raises ValueError if no pair sums to target.
    """
    # Iterate through potential second indices from left to right
    for j in range(1, len(nums)):
        complement = target - nums[j]
        
        # Look for the largest i < j where nums[i] == complement
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                return (i, j)
    
    # No valid pair found
    raise ValueError("No two sum solution")
