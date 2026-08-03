"""
Quicksort implementation using the quicksort algorithm.
"""


def quicksort(lst):
    """
    Sort a list using the quicksort algorithm.
    
    Args:
        lst: A list of comparable elements to sort.
        
    Returns:
        A new sorted list in ascending order.
        
    Raises:
        TypeError: If the list contains non-comparable elements.
    """
    # Input validation
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Base case: lists with 0 or 1 element are already sorted
    if len(lst) <= 1:
        return lst[:]
    
    # Choose pivot (using first element for simplicity and determinism)
    pivot = lst[0]
    
    # Partition into three groups: less than, equal to, greater than pivot
    less = []
    equal = []
    greater = []
    
    for item in lst:
        if item < pivot:
            less.append(item)
        elif item == pivot:
            equal.append(item)
        else:
            greater.append(item)
    
    # Recursively sort and combine
    return quicksort(less) + equal + quicksort(greater)
