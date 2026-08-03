import secrets
from typing import List


def kth_largest(nums: List[int], k: int) -> int:
    """
    Returns the k-th largest value in nums using quickselect.
    
    Args:
        nums: List of integers
        k: Position of the largest element to find (1-indexed, where 1 is the maximum)
    
    Returns:
        The k-th largest element
    
    Raises:
        ValueError: If nums is empty or k is not in range 1..len(nums)
    """
    # Input validation
    if not isinstance(nums, list):
        raise ValueError("nums must be a list")
    
    if not nums:
        raise ValueError("nums cannot be empty")
    
    if not isinstance(k, int):
        raise ValueError("k must be an integer")
    
    if k < 1 or k > len(nums):
        raise ValueError(f"k must be in range 1..{len(nums)}")
    
    # Validate all elements are integers
    for num in nums:
        if not isinstance(num, int):
            raise ValueError("All elements in nums must be integers")
    
    # Create a copy to avoid mutating the input
    arr = nums.copy()
    
    # Convert k-th largest to index in descending order
    # k=1 (largest) -> index 0, k=2 -> index 1, etc.
    target_index = k - 1
    
    # Quickselect algorithm
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # Partition and get pivot index
        pivot_index = partition(arr, left, right)
        
        if pivot_index == target_index:
            return arr[pivot_index]
        elif pivot_index < target_index:
            left = pivot_index + 1
        else:
            right = pivot_index - 1
    
    # Should never reach here with valid input
    raise RuntimeError("Quickselect failed unexpectedly")


def partition(arr: List[int], left: int, right: int) -> int:
    """
    Partition array around a pivot for quickselect.
    Arranges elements in descending order (largest first).
    
    Args:
        arr: Array to partition (modified in place)
        left: Left boundary index
        right: Right boundary index
    
    Returns:
        Final position of the pivot element
    """
    # Use randomized pivot selection to avoid worst-case O(n^2)
    # Use secrets module for cryptographically secure randomness
    pivot_index = left + (secrets.randbelow(right - left + 1) if right > left else 0)
    pivot_value = arr[pivot_index]
    
    # Move pivot to the end
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
    
    # Partition: elements >= pivot go to the left
    store_index = left
    for i in range(left, right):
        if arr[i] >= pivot_value:
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1
    
    # Move pivot to its final position
    arr[store_index], arr[right] = arr[right], arr[store_index]
    
    return store_index
