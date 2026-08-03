def binary_search(arr, target):
    """
    Searches for the target in the sorted list arr using an iterative binary search algorithm.

    Args:
        arr: A sorted list of elements.
        target: The element to search for.

    Returns:
        The index of the target in the list if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoids potential overflow for very large left/right

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:  # arr[mid] > target
            right = mid - 1

    return -1
