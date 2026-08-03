# src/solution.py

def majority_element(nums: list[int]) -> int:
    if not isinstance(nums, list) or not all(isinstance(x, int) for x in nums):
        raise ValueError("Input must be a list of integers.")
    
    n = len(nums)
    if n == 0:
        raise ValueError("Input list cannot be empty.")
    
    # Boyer-Moore Voting Algorithm
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
    
    # Verification pass
    if candidate is not None and nums.count(candidate) > n // 2:
        return candidate
    
    raise ValueError("No strict majority element exists.")
