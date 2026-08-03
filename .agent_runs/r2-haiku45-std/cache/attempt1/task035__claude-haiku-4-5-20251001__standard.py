def has_cycle(sequence):
    """
    Detect if a cycle exists in a next-pointer array.
    
    Args:
        sequence: A list where sequence[i] is the index that node i points to,
                 or -1 meaning node i has no next node (end of the chain).
    
    Returns:
        True if a cycle exists (a node is revisited), False if the chain reaches -1.
    
    Raises:
        ValueError: If any value is < -1 or >= len(sequence) (out-of-bounds index).
    """
    # Empty list returns False
    if not sequence:
        return False
    
    # Validate all indices
    for value in sequence:
        if value < -1 or value >= len(sequence):
            raise ValueError(f"Index {value} is out of bounds for sequence of length {len(sequence)}")
    
    # Follow the pointers starting from index 0
    visited = set()
    current = 0
    
    while True:
        # If we've seen this node before, there's a cycle
        if current in visited:
            return True
        
        # Mark current node as visited
        visited.add(current)
        
        # Get the next node
        next_node = sequence[current]
        
        # If next_node is -1, we've reached the end (no cycle)
        if next_node == -1:
            return False
        
        # Move to the next node
        current = next_node
