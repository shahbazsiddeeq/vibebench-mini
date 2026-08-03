def tail(path, n):
    """
    Returns the last n lines of a file as a list (without newlines).
    
    Args:
        path: Path to the file
        n: Number of lines to return
        
    Returns:
        List of the last n lines (without newlines)
        
    Raises:
        ValueError: If n < 0
        FileNotFoundError: If file does not exist
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    try:
        with open(path, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    if n == 0:
        return []
    
    return lines[-n:] if n > 0 else []
