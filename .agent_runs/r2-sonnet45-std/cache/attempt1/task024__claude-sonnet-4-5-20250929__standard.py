def count_occurrences(arr, target):
    """
    Count occurrences of target in sorted array using binary search.
    
    Args:
        arr: A sorted list
        target: The value to count
        
    Returns:
        The number of times target appears in arr
    """
    if not arr:
        return 0
    
    # Find the leftmost occurrence
    left = 0
    right = len(arr) - 1
    first_pos = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            first_pos = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    # If target not found
    if first_pos == -1:
        return 0
    
    # Find the rightmost occurrence
    left = 0
    right = len(arr) - 1
    last_pos = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            last_pos = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return last_pos - first_pos + 1
