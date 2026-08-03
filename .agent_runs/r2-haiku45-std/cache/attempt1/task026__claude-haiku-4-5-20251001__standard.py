def permutations(lst):
    """
    Returns every ordering of lst as a list of tuples, sorted in ascending order.
    
    Args:
        lst: A list to generate permutations from
        
    Returns:
        A list of tuples representing all permutations, sorted in ascending order
        
    Raises:
        ValueError: If len(lst) > 8
    """
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8")
    
    # Base case: empty list
    if len(lst) == 0:
        return [()]
    
    # Base case: single element
    if len(lst) == 1:
        return [(lst[0],)]
    
    # Recursive case: generate permutations
    result = []
    
    # For each position in the list
    for i in range(len(lst)):
        # Get the element at position i
        element = lst[i]
        
        # Get remaining elements (all except position i)
        remaining = lst[:i] + lst[i+1:]
        
        # Get all permutations of remaining elements
        for perm in permutations(remaining):
            # Add current element to the front of each permutation
            result.append((element,) + perm)
    
    # Sort the result in ascending order
    result.sort()
    
    return result
