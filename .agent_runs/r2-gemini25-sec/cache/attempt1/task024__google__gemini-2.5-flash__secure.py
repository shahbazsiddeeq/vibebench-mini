def count_occurrences(arr, target):
    """
    Counts the number of occurrences of a target value in a sorted list using binary search.

    Args:
        arr: A sorted list of comparable elements.
        target: The value to search for.

    Returns:
        The number of times the target appears in the list.
        Returns 0 if the input list is not a list or is empty, or if target is not found.
    """
    if not isinstance(arr, list):
        raise TypeError("Input 'arr' must be a list.")
    if not arr:
        return 0

    # Validate that the list is sorted. This is O(n) but crucial for correctness
    # and security if the function relies on the sorted property.
    # For very large arrays, this check might be skipped if the caller guarantees sorted input,
    # but for a security-conscious developer, it's safer to validate.
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            raise ValueError("Input 'arr' must be sorted in non-decreasing order.")

    first_occurrence_index = _find_first_occurrence(arr, target)
    if first_occurrence_index == -1:
        return 0

    last_occurrence_index = _find_last_occurrence(arr, target)

    return last_occurrence_index - first_occurrence_index + 1


def _find_first_occurrence(arr, target):
    """
    Finds the index of the first occurrence of the target in a sorted list.
    Returns -1 if the target is not found.
    """
    low = 0
    high = len(arr) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2  # Avoids potential overflow for very large low/high

        if arr[mid] == target:
            result = mid
            high = mid - 1  # Continue searching in the left half for the first occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:  # arr[mid] > target
            high = mid - 1
    return result


def _find_last_occurrence(arr, target):
    """
    Finds the index of the last occurrence of the target in a sorted list.
    Returns -1 if the target is not found.
    """
    low = 0
    high = len(arr) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == target:
            result = mid
            low = mid + 1  # Continue searching in the right half for the last occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:  # arr[mid] > target
            high = mid - 1
    return result
