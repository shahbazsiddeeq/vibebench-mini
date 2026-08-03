# src/solution.py

def count_occurrences(arr, target):
    if not isinstance(arr, list) or not all(isinstance(x, int) for x in arr):
        raise ValueError("Input 'arr' must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("Input 'target' must be an integer.")
    
    left_index = find_left_index(arr, target)
    if left_index == -1:
        return 0
    
    right_index = find_right_index(arr, target)
    
    return right_index - left_index + 1

def find_left_index(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            if mid == 0 or arr[mid - 1] < target:
                return mid
            high = mid - 1
    return -1

def find_right_index(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            if mid == len(arr) - 1 or arr[mid + 1] > target:
                return mid
            low = mid + 1
    return -1
