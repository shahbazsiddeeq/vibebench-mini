import secrets

def quicksort(lst):
    """
    Sorts a list using the Quicksort algorithm.

    Args:
        lst: A list of comparable elements.

    Returns:
        A new list containing the sorted elements.

    Raises:
        TypeError: If the input is not a list or contains non-comparable types.
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list.")

    n = len(lst)
    if n <= 1:
        return list(lst)  # Return a new list for consistency

    # Create a mutable copy to avoid modifying the original list in place
    # and to allow for in-place partitioning.
    arr = list(lst)

    _quicksort_recursive(arr, 0, n - 1)
    return arr

def _quicksort_recursive(arr, low, high):
    """
    Recursive helper function for Quicksort.
    Sorts the sub-array arr[low...high] in place.
    """
    if low < high:
        try:
            pivot_index = _partition(arr, low, high)
            _quicksort_recursive(arr, low, pivot_index - 1)
            _quicksort_recursive(arr, pivot_index + 1, high)
        except TypeError as e:
            # Re-raise TypeError if comparison fails during partitioning
            raise TypeError(f"Elements in the list are not comparable: {e}")

def _partition(arr, low, high):
    """
    Partitions the sub-array arr[low...high] around a pivot.
    Elements smaller than the pivot are moved to its left, and
    elements greater than the pivot are moved to its right.

    Returns:
        The final index of the pivot element.
    """
    # Choose a random pivot to mitigate worst-case scenarios (e.g., already sorted list)
    # Use secrets for cryptographic-quality randomness if available, otherwise random.
    # For this specific problem, secrets.randbelow is appropriate.
    pivot_index = secrets.randbelow(high - low + 1) + low
    pivot_value = arr[pivot_index]

    # Move pivot to the end
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    store_index = low
    for i in range(low, high):
        try:
            if arr[i] < pivot_value:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                store_index += 1
        except TypeError as e:
            # Catch comparison errors and re-raise with a more informative message
            raise TypeError(f"Cannot compare elements '{arr[i]}' and '{pivot_value}': {e}")

    # Move pivot to its final sorted position
    arr[store_index], arr[high] = arr[high], arr[store_index]
    return store_index
