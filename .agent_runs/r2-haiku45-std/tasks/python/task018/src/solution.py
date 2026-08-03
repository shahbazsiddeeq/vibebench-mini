def binary_search(arr, target):
    """
    Returns the index of target in sorted list arr, or -1 if not found.
    Uses iterative binary search implementation.
    
    Args:
        arr: A sorted list of comparable elements
        target: The element to search for
        
    Returns:
        The index of target in arr, or -1 if not found
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_value = arr[mid]
        
        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
