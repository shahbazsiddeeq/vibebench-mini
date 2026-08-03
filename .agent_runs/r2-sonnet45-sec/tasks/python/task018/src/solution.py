def binary_search(arr, target):
    """
    Performs iterative binary search on a sorted list.
    
    Args:
        arr: A sorted list to search in
        target: The value to search for
        
    Returns:
        The index of target in arr if found, -1 otherwise
    """
    # Input validation
    if not isinstance(arr, list):
        return -1
    
    if len(arr) == 0:
        return -1
    
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # Use (left + right) // 2 for mid calculation
        # This is safe from overflow in Python due to arbitrary precision integers
        mid = (left + right) // 2
        
        try:
            mid_value = arr[mid]
        except (IndexError, TypeError):
            return -1
        
        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
