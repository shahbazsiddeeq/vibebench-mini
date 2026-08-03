def quicksort(lst):
    """
    Sorts a list using the quicksort algorithm and returns a new sorted list.

    Args:
        lst: The list to be sorted.

    Returns:
        A new list containing the sorted elements.
    """
    if len(lst) <= 1:
        return list(lst)  # Return a new list for consistency

    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]

    return quicksort(left) + middle + quicksort(right)
