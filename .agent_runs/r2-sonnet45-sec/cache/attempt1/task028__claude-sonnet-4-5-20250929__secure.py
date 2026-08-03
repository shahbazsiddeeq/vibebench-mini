def quicksort(lst):
    """
    Sort a list using the quicksort algorithm.
    
    Args:
        lst: A list of comparable elements
        
    Returns:
        A new sorted list
    """
    # Input validation
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Base case: empty or single element
    if len(lst) <= 1:
        return lst.copy()
    
    # Validate all elements are comparable
    if len(lst) > 1:
        try:
            # Test comparability by attempting comparison
            _ = lst[0] < lst[0]
        except TypeError:
            raise TypeError("List elements must be comparable")
    
    # Create a copy to avoid modifying the original
    return _quicksort_helper(lst.copy())


def _quicksort_helper(lst):
    """
    Internal helper function that performs quicksort in-place.
    
    Args:
        lst: A list to sort (will be modified)
        
    Returns:
        The sorted list
    """
    if len(lst) <= 1:
        return lst
    
    # Choose pivot (middle element to avoid worst case on sorted data)
    pivot_idx = len(lst) // 2
    pivot = lst[pivot_idx]
    
    # Partition into three lists: less than, equal to, and greater than pivot
    less = []
    equal = []
    greater = []
    
    for element in lst:
        try:
            if element < pivot:
                less.append(element)
            elif element > pivot:
                greater.append(element)
            else:
                equal.append(element)
        except TypeError:
            # If comparison fails, raise a clear error
            raise TypeError("List contains incomparable elements")
    
    # Recursively sort and combine
    return _quicksort_helper(less) + equal + _quicksort_helper(greater)
