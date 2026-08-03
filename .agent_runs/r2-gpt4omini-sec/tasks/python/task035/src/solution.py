# src/solution.py

def has_cycle(sequence):
    if not isinstance(sequence, list):
        raise ValueError("Input must be a list.")
    
    n = len(sequence)
    
    # Validate the input values
    for index in sequence:
        if not isinstance(index, int) or index < -1 or index >= n:
            raise ValueError("Index out of bounds or invalid value in sequence.")
    
    visited = set()
    current_index = 0
    
    while current_index != -1:
        if current_index in visited:
            return True
        visited.add(current_index)
        current_index = sequence[current_index]
    
    return False
