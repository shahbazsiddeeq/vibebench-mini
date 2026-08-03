def majority_element(nums: list[int]) -> int:
    if not nums:
        raise ValueError("The list is empty.")
    
    # Boyer-Moore Voting Algorithm
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    
    # Verification pass
    if nums.count(candidate) > len(nums) // 2:
        return candidate
    else:
        raise ValueError("No strict majority element exists.")
