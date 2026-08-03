from __future__ import annotations


def has_cycle(sequence: list[int]) -> bool:
    if not sequence:
        return False
    n = len(sequence)
    if any(idx < -1 or idx >= n for idx in sequence):
        raise ValueError("index out of bounds")
    visited: set[int] = set()
    node = 0
    while node != -1:
        if node in visited:
            return True
        visited.add(node)
        node = sequence[node]
    return False
