# src/solution.py

def binary_search(arr, target):
    if not isinstance(arr, list) or not all(isinstance(x, int) for x in arr):
        raise ValueError("Input must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("Target must be an integer.")
    
    left, right = 0, len(arr) - 1
    
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
