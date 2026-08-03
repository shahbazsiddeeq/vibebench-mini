def count_occurrences(arr, target):
    """
    Count how many times target appears in sorted list arr using binary search.
    
    Time complexity: O(log n)
    Space complexity: O(1)
    
    Args:
        arr: A sorted list
        target: The value to count
        
    Returns:
        The number of times target appears in arr
    """
    if not arr:
        return 0
    
    # Find the leftmost (first) occurrence of target
    def find_left():
        left, right = 0, len(arr) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching in the left half
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    # Find the rightmost (last) occurrence of target
    def find_right():
        left, right = 0, len(arr) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                result = mid
                left = mid + 1  # Continue searching in the right half
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    left_idx = find_left()
    
    # If target not found, return 0
    if left_idx == -1:
        return 0
    
    right_idx = find_right()
    
    # Count is the distance between rightmost and leftmost occurrence + 1
    return right_idx - left_idx + 1
