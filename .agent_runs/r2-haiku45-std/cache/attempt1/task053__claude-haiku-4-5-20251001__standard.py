def count_lines(path: str) -> int:
    """
    Count the number of lines in a UTF-8 text file.
    
    Args:
        path: Path to the file
        
    Returns:
        Number of lines in the file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
