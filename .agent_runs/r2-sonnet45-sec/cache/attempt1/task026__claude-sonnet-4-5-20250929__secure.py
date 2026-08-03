def permutations(lst):
    """
    Returns every ordering of lst as a list of tuples, sorted in ascending order.
    
    Args:
        lst: A list to generate permutations from
        
    Returns:
        A sorted list of tuples representing all permutations
        
    Raises:
        ValueError: If len(lst) > 8
    """
    # Validate input
    if not isinstance(lst, list):
        raise ValueError("Input must be a list")
    
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8")
    
    # Handle empty list
    if len(lst) == 0:
        return [()]
    
    # Generate all permutations recursively
    def generate_perms(elements):
        if len(elements) <= 1:
            return [tuple(elements)]
        
        result = []
        for i in range(len(elements)):
            # Take element at position i
            current = elements[i]
            # Get remaining elements
            remaining = elements[:i] + elements[i+1:]
            # Generate permutations of remaining elements
            for perm in generate_perms(remaining):
                result.append((current,) + perm)
        
        return result
    
    # Generate all permutations
    all_perms = generate_perms(lst)
    
    # Sort and return
    return sorted(all_perms)
