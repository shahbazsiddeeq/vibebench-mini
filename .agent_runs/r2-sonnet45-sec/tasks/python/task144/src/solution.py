def majority_element(nums: list[int]) -> int:
    """
    Returns the value that appears strictly more than len(nums)//2 times.
    
    Uses the Boyer-Moore voting algorithm followed by a verification pass.
    
    Args:
        nums: A list of integers
        
    Returns:
        The majority element (appears > len(nums)//2 times)
        
    Raises:
        ValueError: If nums is empty or if no strict majority element exists
    """
    # Validate input
    if not isinstance(nums, list):
        raise ValueError("Input must be a list")
    
    if len(nums) == 0:
        raise ValueError("Input list cannot be empty")
    
    # Validate all elements are integers
    for item in nums:
        if not isinstance(item, int):
            raise ValueError("All elements must be integers")
    
    # Phase 1: Boyer-Moore Voting Algorithm to find candidate
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    
    # Phase 2: Verification pass
    # Count occurrences of the candidate
    candidate_count = 0
    for num in nums:
        if num == candidate:
            candidate_count += 1
    
    # Check if candidate appears strictly more than len(nums)//2 times
    if candidate_count > len(nums) // 2:
        return candidate
    else:
        raise ValueError("No strict majority element exists")
