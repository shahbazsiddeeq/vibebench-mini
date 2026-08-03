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
    # Validate fields parameter
    if not fields:
        raise ValueError("fields cannot be empty")
    
    for name, start, length in fields:
        if start < 0:
            raise ValueError(f"field start must be >= 0, got {start}")
        if length < 1:
            raise ValueError(f"field length must be >= 1, got {length}")
    
    # Read file with universal newline mode
    # This will raise FileNotFoundError if file doesn't exist
    with open(path, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()
    
    result = []
    
    for line in lines:
        # Remove the newline characters (handles \n, \r\n, \r)
        line = line.rstrip('\r\n')
        
        # Skip empty or whitespace-only lines
        if not line or line.strip() == '':
            continue
        
        # Build dictionary for this line
        record = {}
        for field_name, start, length in fields:
            # Extract field value using slicing (handles short lines gracefully)
            end = start + length
            value = line[start:end]
            # Strip leading and trailing whitespace
            record[field_name] = value.strip()
        
        result.append(record)
    
    return result
