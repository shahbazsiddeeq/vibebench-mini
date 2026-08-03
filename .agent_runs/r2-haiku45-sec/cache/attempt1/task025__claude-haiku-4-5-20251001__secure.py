def rotate(lst, k):
    """
    Returns a new list rotated right by k positions.
    
    Args:
        lst: A list to rotate
        k: Number of positions to rotate right (negative for left rotation)
    
    Returns:
        A new list rotated right by k positions
    
    Raises:
        TypeError: If lst is not a list or k is not an integer
    """
    # Input validation
    if not isinstance(lst, list):
        raise TypeError("First argument must be a list")
    if not isinstance(k, int):
        raise TypeError("Second argument must be an integer")
    
    # Handle empty list
    if len(lst) == 0:
        return []
    
    # Normalize k to be within the range [0, len(lst))
    # Python's modulo operator handles negative numbers correctly
    k = k % len(lst)
    
    # Create a new list (don't modify the original)
    # Rotate right by k: take last k elements and put them at the front
    return lst[-k:] + lst[:-k] if k != 0 else lst[:]
