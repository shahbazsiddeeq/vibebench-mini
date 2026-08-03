def count_occurrences(arr, target):
    """
    Count occurrences of target in sorted array using binary search.
    
    Args:
        arr: A sorted list/sequence
        target: The value to count
        
    Returns:
        int: Number of times target appears in arr
    """
    # Input validation
    if not hasattr(arr, '__len__') or not hasattr(arr, '__getitem__'):
        raise TypeError("arr must be a sequence supporting indexing and len()")
    
    n = len(arr)
    if n == 0:
        return 0
    
    # Find leftmost occurrence using binary search
    def find_left():
        left, right = 0, n - 1
        result = -1
        
        while left <= right:
            mid = left + (right - left) // 2
            mid_val = arr[mid]
            
            if mid_val == target:
                result = mid
                right = mid - 1  # Continue searching left
            elif mid_val < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    # Find rightmost occurrence using binary search
    def find_right():
        left, right = 0, n - 1
        result = -1
        
        while left <= right:
            mid = left + (right - left) // 2
            mid_val = arr[mid]
            
            if mid_val == target:
                result = mid
                left = mid + 1  # Continue searching right
            elif mid_val < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    left_idx = find_left()
    
    # If target not found
    if left_idx == -1:
        return 0
    
    right_idx = find_right()
    
    # Count occurrences
    return right_idx - left_idx + 1
