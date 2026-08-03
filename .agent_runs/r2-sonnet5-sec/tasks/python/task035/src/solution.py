"""
src/solution.py

Detect Cycle (Next-Pointer Array)

Provides has_cycle(sequence) which treats the input list as a "next pointer"
array: sequence[i] is the index the node at position i points to, or -1 if
node i has no successor.

Starting from index 0 and following pointers, returns True if a node is
revisited (cycle detected), or False if the traversal reaches -1 (end of
chain). An empty list returns False.

Raises:
    ValueError: if any value in the sequence is < -1 or >= len(sequence),
        or if the input is not a valid list/sequence of integers.
"""

from typing import List, Sequence, Any


def _validate_sequence(sequence: Any) -> None:
    """
    Validate that `sequence` is a list/tuple of integers where each value
    is either -1 or a valid index within bounds.

    Raises:
        ValueError: on any invalid input, without leaking internal details.
    """
    if not isinstance(sequence, (list, tuple)):
        raise ValueError("Input must be a list or tuple of integers.")

    n = len(sequence)

    for value in sequence:
        # Reject booleans explicitly (bool is a subclass of int) and non-ints
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("All elements must be integers.")
        if value < -1 or value >= n:
            raise ValueError("Index out of bounds in sequence.")


def has_cycle(sequence: Sequence[int]) -> bool:
    """
    Determine whether following next-pointers starting at index 0 leads
    to a cycle.

    Args:
        sequence: A list where sequence[i] is the next index for node i,
            or -1 if there is no next node.

    Returns:
        True if a cycle is detected, False if the chain terminates at -1.

    Raises:
        ValueError: if any value is < -1 or >= len(sequence), or if the
            input is not a valid sequence of integers.
    """
    _validate_sequence(sequence)

    n = len(sequence)
    if n == 0:
        return False

    visited = [False] * n
    current = 0

    while current != -1:
        if visited[current]:
            return True
        visited[current] = True
        current = sequence[current]

    return False
