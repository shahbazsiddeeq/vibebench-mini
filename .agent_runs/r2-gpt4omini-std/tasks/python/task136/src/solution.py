# src/solution.py

def long_lines(source, limit=79):
    if limit < 1:
        raise ValueError("Limit must be at least 1.")
    
    # Split the source into lines using str.splitlines()
    lines = source.splitlines()
    
    # Find the line numbers that exceed the specified limit
    long_line_numbers = [
        index + 1 for index, line in enumerate(lines) if len(line) > limit
    ]
    
    return long_line_numbers
