"""Cycle detection for next-pointer arrays."""

from collections.abc import Sequence
from typing import Any


def has_cycle(sequence: Sequence[int]) -> bool:
    """Return whether the pointer chain starting at index zero contains a cycle.

    Each element must be an integer in ``[-1, len(sequence) - 1]``. The value
    ``-1`` terminates the chain. Invalid elements raise ``ValueError``.
    """
    if isinstance(sequence, (str, bytes, bytearray)) or not isinstance(
        sequence, Sequence
    ):
        raise ValueError("sequence must be a sequence of integer pointers")

    try:
        pointers: tuple[Any, ...] = tuple(sequence)
    except (TypeError, ValueError) as exc:
        raise ValueError("sequence must contain valid integer pointers") from None

    size = len(pointers)
    for pointer in pointers:
        if isinstance(pointer, bool) or not isinstance(pointer, int):
            raise ValueError("all pointers must be integers")
        if pointer < -1 or pointer >= size:
            raise ValueError("pointer is out of bounds")

    if size == 0:
        return False

    visited = bytearray(size)
    current = 0

    while current != -1:
        if visited[current]:
            return True
        visited[current] = 1
        current = pointers[current]

    return False
