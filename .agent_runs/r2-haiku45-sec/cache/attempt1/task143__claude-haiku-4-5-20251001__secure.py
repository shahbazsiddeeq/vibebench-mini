"""
Kth Largest (Quickselect) implementation.

This module provides a secure implementation of the quickselect algorithm
to find the k-th largest element in a list.
"""

import secrets
from typing import List


def kth_largest(nums: List[int], k: int) -> int:
    """
    Find the k-th largest value in nums using quickselect.
    
    Args:
        nums: A list of integers to search.
        k: The rank to find (1-indexed, where k=1 is the maximum).
    
    Returns:
        The k-th largest value in nums.
    
    Raises:
        ValueError: If nums is empty or k is not in range 1..len(nums).
    
    Examples:
        >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
        >>> kth_largest([3, 3, 3], 2)
        3
    """
    # Input validation
    if not isinstance(nums, list):
        raise ValueError("nums must be a list")
    
    if len(nums) == 0:
        raise ValueError("nums cannot be empty")
    
    if not isinstance(k, int):
        raise ValueError("k must be an integer")
    
    if k < 1 or k > len(nums):
        raise ValueError(f"k must be in range 1..{len(nums)}")
    
    # Validate all elements are integers
    for item in nums:
        if not isinstance(item, int):
            raise ValueError("all elements in nums must be integers")
    
    # Create a working copy to avoid mutating the input
    arr = nums[:]
    
    # Convert k to 0-indexed position from the end
    # k=1 (largest) -> index 0 in descending order -> len(arr)-1 in ascending order
    target_index = len(arr) - k
    
    def partition(left: int, right: int, pivot_index: int) -> int:
        """Partition array around pivot and return new pivot index."""
        pivot_value = arr[pivot_index]
        # Move pivot to end
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        store_index = left
        
        # Move all smaller elements to the left
        for i in range(left, right):
            if arr[i] < pivot_value:
                arr[store_index], arr[i] = arr[i], arr[store_index]
                store_index += 1
        
        # Move pivot to its final position
        arr[right], arr[store_index] = arr[store_index], arr[right]
        return store_index
    
    def select(left: int, right: int, target: int) -> int:
        """Quickselect to find element at target index."""
        if left == right:
            return arr[left]
        
        # Choose random pivot for better average performance
        pivot_index = left + secrets.randbelow(right - left + 1)
        pivot_index = partition(left, right, pivot_index)
        
        if target == pivot_index:
            return arr[target]
        elif target < pivot_index:
            return select(left, pivot_index - 1, target)
        else:
            return select(pivot_index + 1, right, target)
    
    return select(0, len(arr) - 1, target_index)
