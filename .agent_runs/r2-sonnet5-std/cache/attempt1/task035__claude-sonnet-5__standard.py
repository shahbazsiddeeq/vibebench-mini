def has_cycle(sequence):
    n = len(sequence)
    for val in sequence:
        if val < -1 or val >= n:
            raise ValueError(f"Invalid pointer value: {val}")

    if n == 0:
        return False

    visited = set()
    current = 0
    while current != -1:
        if current in visited:
            return True
        visited.add(current)
        current = sequence[current]

    return False
