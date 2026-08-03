def majority_element(nums: list[int]) -> int:
    """
    Returns the value that appears strictly more than len(nums)//2 times.
    Uses Boyer-Moore voting algorithm followed by verification.
    
    Args:
        nums: List of integers
        
    Returns:
        The majority element
        
    Raises:
        ValueError: If nums is empty or no strict majority element exists
    """
    if not nums:
        raise ValueError("Input list is empty")
    
    # Phase 1: Boyer-Moore voting to find candidate
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
    
    # Phase 2: Verification - count occurrences of candidate
    candidate_count = sum(1 for num in nums if num == candidate)
    
    # Check if candidate appears strictly more than len(nums)//2 times
    if candidate_count > len(nums) // 2:
        return candidate
    else:
        raise ValueError("No strict majority element exists")
