def binary_search(arr, target):
    """
    Iterative binary search.

    Returns the index of target in sorted list arr, or -1 if not found.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
