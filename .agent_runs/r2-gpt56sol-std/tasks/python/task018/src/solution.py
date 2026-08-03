def binary_search(arr, target):
    """Return the index of target in sorted arr, or -1 if it is absent."""
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2
        value = arr[mid]

        if value == target:
            return mid
        if value < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
