def has_cycle(sequence):
    if not sequence:
        return False
    
    visited = set()
    index = 0
    
    while index != -1:
        if index in visited:
            return True
        if index < -1 or index >= len(sequence):
            raise ValueError("Index out of bounds")
        
        visited.add(index)
        index = sequence[index]
    
    return False
