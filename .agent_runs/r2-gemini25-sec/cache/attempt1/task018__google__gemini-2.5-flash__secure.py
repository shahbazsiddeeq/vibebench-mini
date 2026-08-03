def binary_search(arr, target):
    """
    Searches for a target value in a sorted list using the binary search algorithm.

    Args:
        arr: A list of numbers sorted in ascending order.
        target: The number to search for.

    Returns:
        The index of the target in the list if found, otherwise -1.
    """
    if not isinstance(arr, (list, tuple)):
        raise TypeError("Input 'arr' must be a list or tuple.")
    if not all(isinstance(x, (int, float)) for x in arr):
        raise ValueError("All elements in 'arr' must be numbers.")
    if not isinstance(target, (int, float)):
        raise TypeError("Input 'target' must be a number.")

    # Basic check for sorted property (can be expensive for large lists,
    # but good for security to ensure preconditions are met if not guaranteed by context)
    if len(arr) > 1:
        for i in range(len(arr) - 1):
            if arr[i] > arr[i+1]:
                raise ValueError("Input 'arr' must be sorted in ascending order.")

    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2  # Avoids potential overflow for very large low/high

        # Ensure mid is within valid bounds, though it should be by construction
        if not (0 <= mid < len(arr)):
            # This case should ideally not be reached with correct low/high management
            # but serves as a defensive check.
            return -1 

        mid_val = arr[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
