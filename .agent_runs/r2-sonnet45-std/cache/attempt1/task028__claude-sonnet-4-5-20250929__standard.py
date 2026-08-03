def quicksort(lst):
    """
    Sort a list using the quicksort algorithm.
    
    Args:
        lst: A list of comparable elements
        
    Returns:
        A new sorted list
    """
    # Base case: lists with 0 or 1 elements are already sorted
    if len(lst) <= 1:
        return lst[:]
    
    # Choose pivot (using middle element for better average performance)
    pivot_index = len(lst) // 2
    pivot = lst[pivot_index]
    
    # Partition the list into three parts:
    # - elements less than pivot
    # - elements equal to pivot
    # - elements greater than pivot
    less = []
    equal = []
    greater = []
    
    for element in lst:
        if element < pivot:
            less.append(element)
        elif element > pivot:
            greater.append(element)
        else:
            equal.append(element)
    
    # Recursively sort the less and greater partitions
    # and concatenate: sorted(less) + equal + sorted(greater)
    return quicksort(less) + equal + quicksort(greater)
