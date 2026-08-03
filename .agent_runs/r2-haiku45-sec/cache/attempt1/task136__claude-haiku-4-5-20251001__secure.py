def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters 
    (excluding the line terminator) is strictly greater than limit.
    
    Lines are obtained with Python's str.splitlines(), which recognizes
    "\n", "\r", "\r\n" (each a single terminator), plus form feed "\f",
    vertical tab "\v", and other Unicode line boundaries.
    
    Args:
        source: A string to analyze
        limit: Maximum allowed line length (default 79). Must be >= 1.
        
    Returns:
        A list of 1-based line numbers that exceed the limit.
        
    Raises:
        ValueError: If limit < 1
    """
    if limit < 1:
        raise ValueError("limit must be >= 1")
    
    lines = source.splitlines()
    result = []
    
    for line_num, line in enumerate(lines, start=1):
        if len(line) > limit:
            result.append(line_num)
    
    return result
