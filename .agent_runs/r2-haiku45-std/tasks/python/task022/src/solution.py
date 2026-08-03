def two_sum(nums, target):
    """
    Returns a tuple (i, j) with i < j such that nums[i] + nums[j] == target.
    When more than one valid pair exists, returns the pair with the smallest 
    second index j; among indices that could pair with that j, uses the largest i.
    
    Raises ValueError if no pair sums to target.
    """
    # Dictionary to store the most recent index of each value seen so far
    seen = {}
    
    for j in range(len(nums)):
        complement = target - nums[j]
        
        # Check if the complement was seen before index j
        if complement in seen:
            i = seen[complement]
            return (i, j)
        
        # Record the current value and its index
        # We update even if we've seen this value before, to keep the most recent index
        seen[nums[j]] = j
    
    # No valid pair found
    raise ValueError(f"No pair sums to target {target}")
