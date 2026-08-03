def has_cycle(sequence):
    """Return whether the next-pointer chain starting at index 0 contains a cycle."""
    length = len(sequence)

    for pointer in sequence:
        if pointer < -1 or pointer >= length:
            raise ValueError(f"Invalid next-pointer index: {pointer}")

    if length == 0:
        return False

    visited = set()
    current = 0

    while current != -1:
        if current in visited:
            return True
        visited.add(current)
        current = sequence[current]

    return False
