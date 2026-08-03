def binary_search(arr, target):
    """
    Performs binary search on a sorted list to find the target value.
    
    Args:
        arr: A sorted list of comparable elements
        target: The value to search for
        
    Returns:
        The index of target in arr if found, otherwise -1
        
    Raises:
        TypeError: If arr is not a list-like object or target type is incompatible
    """
    # Input validation
    if not hasattr(arr, '__getitem__') or not hasattr(arr, '__len__'):
        raise TypeError("arr must be a list-like object")
    
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        mid_value = arr[mid]
        
        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
