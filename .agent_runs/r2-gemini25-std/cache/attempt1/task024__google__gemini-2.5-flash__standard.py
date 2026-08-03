def _find_first(arr, target):
    """
    Finds the first occurrence of the target in a sorted array using binary search.
    Returns the index of the first occurrence, or -1 if not found.
    """
    low = 0
    high = len(arr) - 1
    first_occurrence = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            first_occurrence = mid
            high = mid - 1  # Try to find an earlier occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return first_occurrence

def _find_last(arr, target):
    """
    Finds the last occurrence of the target in a sorted array using binary search.
    Returns the index of the last occurrence, or -1 if not found.
    """
    low = 0
    high = len(arr) - 1
    last_occurrence = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            last_occurrence = mid
            low = mid + 1  # Try to find a later occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return last_occurrence

def count_occurrences(arr, target):
    """
    Counts how many times target appears in sorted list arr using binary search.
    Returns the number of occurrences.
    """
    if not arr:
        return 0

    first_idx = _find_first(arr, target)
    if first_idx == -1:
        return 0  # Target not found

    last_idx = _find_last(arr, target)
    
    # The number of occurrences is (last_index - first_index + 1)
    return last_idx - first_idx + 1
