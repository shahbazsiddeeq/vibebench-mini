"""
Sliding Window Maximum implementation.

This module provides a function to find the maximum value in each
sliding window of a given size over a list of numbers.
"""

from collections import deque
from typing import List


def sliding_max(nums: List[int], k: int) -> List[int]:
    """
    Return a list of maximum values for each window of size k.
    
    Args:
        nums: A list of integers.
        k: The window size (must be positive and <= len(nums)).
    
    Returns:
        A list of maximum values, one for each window position.
    
    Raises:
        ValueError: If k <= 0 or k > len(nums).
    """
    # Input validation
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer")
    
    if k > len(nums):
        raise ValueError("k cannot be larger than the length of nums")
    
    if not nums:
        return []
    
    # Use a deque to maintain indices of useful elements
    # The deque stores indices in decreasing order of their values
    dq: deque = deque()
    result: List[int] = []
    
    for i in range(len(nums)):
        # Remove indices that are outside the current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove elements from the back while the current element is larger
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        # Add current element's index
        dq.append(i)
        
        # Once we've processed at least k elements, add the max to result
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
