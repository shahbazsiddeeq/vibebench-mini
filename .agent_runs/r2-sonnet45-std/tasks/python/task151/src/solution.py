def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    """
    Parse a fixed-width text file into a list of dictionaries.
    
    Args:
        path: Path to the UTF-8 text file
        fields: List of (name, start, length) tuples defining field positions
        
    Returns:
        List of dictionaries, one per non-blank line
        
    Raises:
        FileNotFoundError: If path does not exist
        ValueError: If fields is empty or any field has invalid start/length
    """
    # Validate fields
    if not fields:
        raise ValueError("fields cannot be empty")
    
    for name, start, length in fields:
        if start < 0:
            raise ValueError(f"field start must be >= 0, got {start}")
        if length < 1:
            raise ValueError(f"field length must be >= 1, got {length}")
    
    # Read file with universal newline mode (default for text mode)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    
    for line in lines:
        # Remove the newline character(s) at the end
        line = line.rstrip('\n\r')
        
        # Skip blank or whitespace-only lines
        if not line.strip():
            continue
        
        # Build dictionary for this line
        record = {}
        for name, start, length in fields:
            # Extract field value (slicing past end is safe in Python)
            value = line[start:start + length]
            # Strip leading and trailing whitespace
            record[name] = value.strip()
        
        result.append(record)
    
    return result
