def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters 
    (excluding the line terminator) is strictly greater than limit.
    
    Lines are obtained with Python's str.splitlines().
    Raises ValueError if limit < 1.
    """
    if limit < 1:
        raise ValueError("limit must be >= 1")
    
    lines = source.splitlines()
    result = []
    
    for line_num, line in enumerate(lines, start=1):
        if len(line) > limit:
            result.append(line_num)
    
    return result
