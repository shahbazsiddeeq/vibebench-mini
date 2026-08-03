def has_cycle(sequence):
    """
    Detects if a cycle exists in a next-pointer array.

    The sequence is treated as a next-pointer array where sequence[i] is the
    index that node i points to, or -1 meaning node i has no next node (end of the chain).
    Starting from index 0, follow the pointers and return True if a node is
    revisited (a cycle exists), or False if the chain reaches a -1 (no next node).

    Args:
        sequence (list): A list of integers representing next pointers.

    Returns:
        bool: True if a cycle exists, False otherwise.

    Raises:
        ValueError: If any value in the sequence is < -1 or >= len(sequence)
                    (an out-of-bounds index).
    """
    n = len(sequence)

    if n == 0:
        return False

    # Validate input values
    for i, val in enumerate(sequence):
        if not (-1 <= val < n):
            raise ValueError(f"Invalid pointer value at index {i}: {val}. Must be between -1 and {n-1}.")

    # Use Floyd's Cycle-Finding Algorithm (Tortoise and Hare)
    # Initialize two pointers, slow and fast, at the start of the sequence (index 0).
    slow = 0
    fast = 0

    while True:
        # Move slow pointer one step
        slow_next = sequence[slow]
        if slow_next == -1:
            return False  # Slow pointer reached the end, no cycle
        slow = slow_next

        # Move fast pointer two steps
        fast_next1 = sequence[fast]
        if fast_next1 == -1:
            return False  # Fast pointer reached the end, no cycle
        
        fast_next2 = sequence[fast_next1]
        if fast_next2 == -1:
            return False  # Fast pointer reached the end on its second step, no cycle
        
        fast = fast_next2

        # Check for cycle
        if slow == fast:
            return True
