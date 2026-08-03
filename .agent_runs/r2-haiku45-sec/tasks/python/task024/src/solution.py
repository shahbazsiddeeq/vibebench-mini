"""
Binary search-based solution for counting occurrences in a sorted array.
"""


def count_occurrences(arr, target):
    """
    Count how many times target appears in sorted list arr using binary search.
    
    Time complexity: O(log n)
    Space complexity: O(1)
    
    Args:
        arr: A sorted list/sequence of comparable elements
        target: The value to count
        
    Returns:
        The number of times target appears in arr
    """
    if not arr:
        return 0
    
    # Find the leftmost (first) occurrence of target
    left_pos = _find_leftmost(arr, target)
    
    # If target not found, return 0
    if left_pos == -1:
        return 0
    
    # Find the rightmost (last) occurrence of target
    right_pos = _find_rightmost(arr, target)
    
    # Count is the distance between rightmost and leftmost positions
    return right_pos - left_pos + 1


def _find_leftmost(arr, target):
    """
    Find the leftmost (first) index of target in sorted array.
    Returns -1 if target is not found.
    
    Time complexity: O(log n)
    """
    left = 0
    right = len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = arr[mid]
        
        if mid_val == target:
            result = mid
            # Continue searching in the left half to find the leftmost occurrence
            right = mid - 1
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def _find_rightmost(arr, target):
    """
    Find the rightmost (last) index of target in sorted array.
    Assumes target exists in arr (should only be called after confirming existence).
    
    Time complexity: O(log n)
    """
    left = 0
    right = len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = arr[mid]
        
        if mid_val == target:
            result = mid
            # Continue searching in the right half to find the rightmost occurrence
            left = mid + 1
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result
