def binary_search(arr, target):
    """
    Performs iterative binary search on a sorted array.
    
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
        mid_val = arr[mid]
        
        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
