"""
Majority Element finder using Boyer-Moore Voting Algorithm.

This module implements the Boyer-Moore voting algorithm to find the majority element
in a list of integers. The majority element is defined as an element that appears
strictly more than len(nums)//2 times.
"""

from typing import List


def majority_element(nums: List[int]) -> int:
    """
    Find the majority element in a list using Boyer-Moore voting algorithm.
    
    The majority element is defined as an element that appears strictly more than
    len(nums)//2 times.
    
    Args:
        nums: A list of integers to search for the majority element.
        
    Returns:
        The majority element (an integer).
        
    Raises:
        ValueError: If nums is empty or if no strict majority element exists.
    """
    # Input validation
    if not isinstance(nums, list):
        raise ValueError("Input must be a list")
    
    if len(nums) == 0:
        raise ValueError("List cannot be empty")
    
    # Validate all elements are integers
    for num in nums:
        if not isinstance(num, int) or isinstance(num, bool):
            raise ValueError("All elements must be integers")
    
    # Boyer-Moore Voting Algorithm - Phase 1: Find candidate
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
    
    # Phase 2: Verification pass - verify the candidate is a strict majority
    if candidate is None:
        raise ValueError("No majority element found")
    
    majority_count = sum(1 for num in nums if num == candidate)
    threshold = len(nums) // 2
    
    if majority_count > threshold:
        return candidate
    else:
        raise ValueError("No majority element found")
