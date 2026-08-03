def rotate(lst, k):
    """
    Rotate a list right by k positions.
    
    Args:
        lst: The list to rotate
        k: Number of positions to rotate right (negative for left rotation)
    
    Returns:
        A new list rotated by k positions
    """
    if not lst:
        return []
    
    n = len(lst)
    # Normalize k to be within [0, n)
    k = k % n
    
    # Right rotation by k means: last k elements + first (n-k) elements
    return lst[-k:] + lst[:-k] if k != 0 else lst[:]
