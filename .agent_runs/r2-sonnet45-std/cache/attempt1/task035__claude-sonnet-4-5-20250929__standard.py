def has_cycle(sequence):
    """
    Detect if there's a cycle in a next-pointer array.
    
    Args:
        sequence: A list where sequence[i] is the index that node i points to,
                 or -1 meaning node i has no next node.
    
    Returns:
        True if a cycle exists, False otherwise.
        
    Raises:
        ValueError: If any value is < -1 or >= len(sequence).
    """
    # Empty list returns False
    if not sequence:
        return False
    
    # Validate all values are within bounds
    n = len(sequence)
    for value in sequence:
        if value < -1 or value >= n:
            raise ValueError(f"Index out of bounds: {value}")
    
    # Track visited nodes
    visited = set()
    current = 0
    
    # Follow the chain starting from index 0
    while current != -1:
        # If we've seen this node before, we have a cycle
        if current in visited:
            return True
        
        # Mark current node as visited
        visited.add(current)
        
        # Move to next node
        current = sequence[current]
    
    # Reached -1 (end of chain) without finding a cycle
    return False
