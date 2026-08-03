def long_lines(source, limit=79):
    if limit < 1:
        raise ValueError("Limit must be at least 1.")
    
    long_line_numbers = []
    lines = source.splitlines()
    
    for index, line in enumerate(lines):
        if len(line) > limit:
            long_line_numbers.append(index + 1)
    
    return long_line_numbers
