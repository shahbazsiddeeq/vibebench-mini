def power_set(elements):
    """
    Generate the power set of the input list.
    
    Args:
        elements: A list of elements (may contain duplicates)
    
    Returns:
        A list of frozensets representing all subsets, sorted by size then lexicographically
    """
    # Input validation
    if not isinstance(elements, list):
        raise TypeError("Input must be a list")
    
    # Remove duplicates by converting to set
    unique_elements = list(set(elements))
    
    # Generate all subsets using bit manipulation
    n = len(unique_elements)
    power_set_list = []
    
    # Generate 2^n subsets
    for i in range(1 << n):  # 2^n combinations
        subset = []
        for j in range(n):
            # Check if j-th bit is set in i
            if i & (1 << j):
                subset.append(unique_elements[j])
        power_set_list.append(frozenset(subset))
    
    # Sort by size first, then lexicographically by string representation
    def sort_key(fs):
        # First sort by size
        size = len(fs)
        # Then by lexicographically sorted string representations of elements
        if size == 0:
            return (size, [])
        else:
            # Convert elements to strings and sort them
            sorted_str_elements = sorted(str(elem) for elem in fs)
            return (size, sorted_str_elements)
    
    power_set_list.sort(key=sort_key)
    
    return power_set_list
