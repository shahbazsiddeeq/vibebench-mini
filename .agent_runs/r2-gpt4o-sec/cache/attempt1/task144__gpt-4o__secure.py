# src/solution.py

from typing import List
from collections import Counter

def majority_element(nums: List[int]) -> int:
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
    if candidate is not None:
        count = Counter(nums)
        if count[candidate] > len(nums) // 2:
            return candidate
    
    raise ValueError("No majority element found.")
