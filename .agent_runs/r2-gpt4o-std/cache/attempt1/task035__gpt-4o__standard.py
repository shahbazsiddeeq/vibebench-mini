def has_cycle(sequence):
    if not sequence:
        return False

    visited = set()
    current_index = 0

    while current_index != -1:
        if current_index in visited:
            return True
        if current_index < -1 or current_index >= len(sequence):
            raise ValueError("Index out of bounds")
        
        visited.add(current_index)
        current_index = sequence[current_index]

    return False
