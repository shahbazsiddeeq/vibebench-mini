import collections

def has_cycle(sequence: list) -> bool:
    """
    Detects if a cycle exists in a next-pointer array.

    The sequence is treated as a next-pointer array where sequence[i] is the
    index that node i points to, or -1 meaning node i has no next node (end of the chain).
    Starting from index 0, the function follows the pointers and returns True if a node
    is revisited (a cycle exists), or False if the chain reaches a -1 (no next node).

    Args:
        sequence: A list of integers representing the next-pointer array.

    Returns:
        True if a cycle exists, False otherwise.

    Raises:
        ValueError: If any value in the sequence is < -1 or >= len(sequence)
                    (an out-of-bounds index).
    """
    n = len(sequence)

    if n == 0:
        return False

    # Input validation
    for i, val in enumerate(sequence):
        if not isinstance(val, int):
            raise ValueError(f"Invalid input: sequence must contain only integers, found {type(val)} at index {i}.")
        if val < -1 or val >= n:
            raise ValueError(f"Invalid pointer value at index {i}: {val}. Must be between -1 and {n-1}.")

    # Use Floyd's Cycle-Finding Algorithm (Tortoise and Hare)
    # Initialize two pointers, slow and fast, at the start of the sequence (index 0).
    slow = 0
    fast = 0

    while True:
        # Move slow pointer one step
        if slow == -1:  # Reached end of chain
            return False
        slow = sequence[slow]

        # Move fast pointer two steps
        if fast == -1:  # Reached end of chain
            return False
        fast = sequence[fast]
        if fast == -1:  # Reached end of chain after first step
            return False
        fast = sequence[fast]

        # If slow and fast pointers meet, a cycle is detected.
        if slow == fast:
            return True
