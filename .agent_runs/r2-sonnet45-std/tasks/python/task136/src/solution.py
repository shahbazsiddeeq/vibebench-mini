def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters 
    (excluding the line terminator) is strictly greater than limit.
    
    Args:
        source: The source text to check
        limit: Maximum allowed line length (default 79)
        
    Returns:
        List of 1-based line numbers that exceed the limit
        
    Raises:
        ValueError: If limit < 1
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")
    
    lines = source.splitlines()
    result = []
    
    for i, line in enumerate(lines, start=1):
        if len(line) > limit:
            result.append(i)
    
    return result
