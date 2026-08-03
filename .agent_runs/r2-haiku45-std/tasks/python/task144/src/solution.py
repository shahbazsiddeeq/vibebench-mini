def majority_element(nums: list[int]) -> int:
    """
    Find the majority element using Boyer-Moore voting algorithm.
    
    Returns the value that appears strictly more than len(nums)//2 times.
    Raises ValueError if nums is empty or if no strict majority element exists.
    
    Args:
        nums: A list of integers
        
    Returns:
        The majority element
        
    Raises:
        ValueError: If nums is empty or no strict majority element exists
    """
    if not nums:
        raise ValueError("nums is empty")
    
    # Boyer-Moore voting algorithm - find candidate
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
    
    # Verification pass - check if candidate is actually a majority element
    majority_threshold = len(nums) // 2
    candidate_count = sum(1 for num in nums if num == candidate)
    
    if candidate_count > majority_threshold:
        return candidate
    else:
        raise ValueError("No strict majority element exists")
