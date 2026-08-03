def has_cycle(sequence):
    """
    Detect if a next-pointer array contains a cycle.
    
    Args:
        sequence: A list where sequence[i] is the index that node i points to,
                 or -1 meaning node i has no next node (end of the chain).
    
    Returns:
        True if a cycle exists (a node is revisited), False if the chain reaches -1.
    
    Raises:
        ValueError: If any value is < -1 or >= len(sequence) (out-of-bounds index).
    """
    # Handle empty list
    if not sequence:
        return False
    
    # Validate all values in the sequence
    for value in sequence:
        if not isinstance(value, int):
            raise ValueError(f"Invalid value in sequence: {value} is not an integer")
        if value < -1 or value >= len(sequence):
            raise ValueError(f"Out-of-bounds index: {value}")
    
    # Track visited nodes to detect cycles
    visited = set()
    current = 0
    
    # Follow the pointers starting from index 0
    while True:
        # If we've seen this node before, there's a cycle
        if current in visited:
            return True
        
        # Mark current node as visited
        visited.add(current)
        
        # Get the next node index
        next_node = sequence[current]
        
        # If next_node is -1, we've reached the end (no cycle)
        if next_node == -1:
            return False
        
        # Move to the next node
        current = next_node
