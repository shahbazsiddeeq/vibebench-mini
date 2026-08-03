def has_cycle(sequence):
    """
    Detect if a cycle exists in a next-pointer array.
    
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
    
    # Validate all indices first
    n = len(sequence)
    for i, next_idx in enumerate(sequence):
        if not isinstance(next_idx, int):
            raise ValueError(f"Invalid value at index {i}: must be an integer")
        if next_idx < -1 or next_idx >= n:
            raise ValueError(f"Invalid index at position {i}: {next_idx} is out of bounds")
    
    # Track visited nodes
    visited = set()
    current = 0
    
    # Follow the chain from index 0
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
