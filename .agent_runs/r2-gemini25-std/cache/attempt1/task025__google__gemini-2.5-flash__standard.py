def rotate(lst, k):
    """
    Rotates a list to the right by k positions.

    Args:
        lst: The input list.
        k: The number of positions to rotate. Positive k means right rotation,
           negative k means left rotation.

    Returns:
        A new list rotated right by k positions.
    """
    if not lst:
        return []

    n = len(lst)
    # Calculate the effective rotation amount.
    # k % n handles cases where k is larger than n or negative.
    # A negative k % n result means a left rotation.
    # For example, if k = -7 and n = 5, k % n = -2.
    # To convert this to a right rotation equivalent, we add n: -2 + 5 = 3.
    # So, -7 left rotation is equivalent to 3 right rotation.
    effective_k = k % n
    if effective_k < 0:
        effective_k += n

    # Slice the list to perform the rotation
    # The last 'effective_k' elements come first, followed by the remaining elements.
    return lst[n - effective_k:] + lst[:n - effective_k]
