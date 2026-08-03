def rotate(lst, k):
    """
    Returns a new list rotated right by k positions.
    
    Args:
        lst: The input list to rotate
        k: Number of positions to rotate right (negative for left rotation)
    
    Returns:
        A new list rotated right by k positions
    """
    if not lst:
        return []
    
    # Normalize k to be within the range [0, len(lst))
    # Python's modulo handles negative numbers correctly
    k = k % len(lst)
    
    # Rotate right by k: take last k elements and put them at the front
    return lst[-k:] + lst[:-k] if k != 0 else lst[:]
