from collections import deque
from typing import List


def sliding_max(nums: List[int], k: int) -> List[int]:
    """
    Returns a list of maximum values for each window of size k.
    
    Args:
        nums: List of integers to process
        k: Window size
        
    Returns:
        List of maximum values for each window
        
    Raises:
        ValueError: If k <= 0 or k > len(nums)
    """
    # Input validation
    if not isinstance(nums, list):
        raise ValueError("nums must be a list")
    
    if not isinstance(k, int):
        raise ValueError("k must be an integer")
    
    if k <= 0:
        raise ValueError("k must be greater than 0")
    
    if k > len(nums):
        raise ValueError("k cannot be greater than the length of nums")
    
    # Validate all elements in nums are integers or floats
    for num in nums:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements in nums must be numeric")
    
    # Handle edge case where k equals length of nums
    if k == len(nums):
        return [max(nums)]
    
    result = []
    # Deque stores indices of elements in current window
    # Elements are stored in decreasing order of their values
    dq = deque()
    
    # Process first window
    for i in range(k):
        # Remove elements from back while current element is greater
        while dq and nums[i] >= nums[dq[-1]]:
            dq.pop()
        dq.append(i)
    
    # The front of deque has the maximum of first window
    result.append(nums[dq[0]])
    
    # Process remaining elements
    for i in range(k, len(nums)):
        # Remove elements outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove elements from back while current element is greater
        while dq and nums[i] >= nums[dq[-1]]:
            dq.pop()
        
        dq.append(i)
        result.append(nums[dq[0]])
    
    return result
