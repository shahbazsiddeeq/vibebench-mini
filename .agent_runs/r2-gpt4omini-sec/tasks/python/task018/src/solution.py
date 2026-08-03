# src/solution.py

def binary_search(arr, target):
    # Validate input types
    if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
        raise ValueError("arr must be a list of numbers.")
    if not isinstance(target, (int, float)):
        raise ValueError("target must be a number.")

    # Ensure the array is sorted
    arr = sorted(arr)

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
