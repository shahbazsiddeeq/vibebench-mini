def rotate(lst, k):
    """
    Rotate a list right by k positions.
    
    Args:
        lst: The list to rotate
        k: Number of positions to rotate right (negative for left rotation)
    
    Returns:
        A new list rotated by k positions
    
    Raises:
        TypeError: If lst is not a list or k is not an integer
    """
    # Input validation
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(k, int):
        raise TypeError("k must be an integer")
    
    # Handle empty list
    if not lst:
        return []
    
    # Calculate effective rotation (handle k larger than length and negative k)
    n = len(lst)
    k = k % n
    
    # Perform rotation by slicing (creates a new list, doesn't modify original)
    if k == 0:
        return lst[:]
    
    # Right rotation by k is equivalent to taking last k elements + first (n-k) elements
    return lst[-k:] + lst[:-k]
