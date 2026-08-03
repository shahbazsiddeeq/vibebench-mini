def has_cycle(sequence):
    if not isinstance(sequence, list):
        raise ValueError("Input must be a list.")
    
    n = len(sequence)
    if n == 0:
        return False

    for index in sequence:
        if not isinstance(index, int) or index < -1 or index >= n:
            raise ValueError("All indices must be integers between -1 and len(sequence) - 1.")

    visited = set()
    current = 0

    while current != -1:
        if current in visited:
            return True
        visited.add(current)
        current = sequence[current]

    return False
