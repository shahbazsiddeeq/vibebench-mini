def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    """
    Parse a fixed-width record file.
    
    Args:
        path: Path to the text file to parse
        fields: List of tuples (name, start, length) defining field positions
        
    Returns:
        List of dictionaries, one per non-blank line, with field values stripped
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If fields is empty or any field has invalid start/length
    """
    # Validate fields
    if not fields:
        raise ValueError("fields cannot be empty")
    
    for name, start, length in fields:
        if start < 0:
            raise ValueError(f"field '{name}' has start < 0")
        if length < 1:
            raise ValueError(f"field '{name}' has length < 1")
    
    # Read file with universal newline mode
    try:
        with open(path, 'r', encoding='utf-8', newline=None) as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    result = []
    
    for line in lines:
        # Remove the newline character(s) if present
        line = line.rstrip('\n\r')
        
        # Skip empty or whitespace-only lines
        if not line or line.isspace():
            continue
        
        # Build dictionary for this line
        record = {}
        for name, start, length in fields:
            # Extract substring (slicing past end is safe in Python)
            value = line[start:start + length]
            # Strip leading and trailing whitespace
            value = value.strip()
            record[name] = value
        
        result.append(record)
    
    return result
