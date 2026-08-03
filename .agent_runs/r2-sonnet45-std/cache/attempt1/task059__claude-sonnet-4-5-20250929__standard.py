def tail(path, n):
    """
    Returns the last n lines of a file as a list (without newlines).
    
    Args:
        path: Path to the file
        n: Number of lines to return from the end
        
    Returns:
        List of strings representing the last n lines (without newlines)
        
    Raises:
        ValueError: If n < 0
        FileNotFoundError: If the file doesn't exist
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n == 0:
        return []
    
    # This will raise FileNotFoundError if the file doesn't exist
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    
    # Return the last n lines (or all lines if n > length)
    return lines[-n:] if lines else []
