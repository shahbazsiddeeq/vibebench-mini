def quicksort(lst):
    """
    Sort a list using the quicksort algorithm.
    
    Args:
        lst: A list to be sorted
        
    Returns:
        A new sorted list
    """
    if len(lst) <= 1:
        return lst
    
    # Choose pivot as the middle element
    pivot = lst[len(lst) // 2]
    
    # Partition into three lists: less, equal, greater
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
