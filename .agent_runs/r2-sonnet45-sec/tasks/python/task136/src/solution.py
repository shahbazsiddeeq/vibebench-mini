def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters 
    (excluding the line terminator) is strictly greater than limit.
    
    Args:
        source: The source code string to check
        limit: Maximum allowed line length (default 79)
        
    Returns:
        List of 1-based line numbers that exceed the limit
        
    Raises:
        ValueError: If limit < 1
    """
    # Validate input
    if not isinstance(limit, int):
        raise ValueError("limit must be an integer")
    
    if limit < 1:
        raise ValueError("limit must be at least 1")
    
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    # Split source into lines using Python's splitlines()
    # This handles \n, \r, \r\n, \f, \v, and other Unicode line boundaries
    lines = source.splitlines()
    
    # Find line numbers (1-based) where length > limit
    result = []
    for line_num, line in enumerate(lines, start=1):
        if len(line) > limit:
            result.append(line_num)
    
    return result
