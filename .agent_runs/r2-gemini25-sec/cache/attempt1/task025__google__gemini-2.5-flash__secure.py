def rotate(lst, k):
    """
    Rotates a list to the right by k positions.

    Args:
        lst: The input list.
        k: The number of positions to rotate. Positive k means right rotation,
           negative k means left rotation.

    Returns:
        A new list rotated right by k positions.
        Returns an empty list if the input list is empty.
        Returns a copy of the original list if k is 0.

    Raises:
        TypeError: If lst is not a list or k is not an integer.
    """
    if not isinstance(lst, list):
        raise TypeError("Input 'lst' must be a list.")
    if not isinstance(k, int):
        raise TypeError("Input 'k' must be an integer.")

    n = len(lst)
    if n == 0:
        return []

    # Calculate the effective rotation amount.
    # The modulo operator handles both positive and negative k correctly
    # for the purpose of finding the effective shift.
    # For example, -7 % 5 = 3 in Python, which is the desired right shift.
    effective_k = k % n

    # If effective_k is 0, no rotation is needed, return a copy to be safe.
    if effective_k == 0:
        return list(lst)

    # Perform the rotation by slicing and concatenating.
    # The list is split into two parts:
    # 1. The last 'effective_k' elements.
    # 2. The first 'n - effective_k' elements.
    # These parts are then concatenated in reverse order.
    return lst[n - effective_k:] + lst[:n - effective_k]
