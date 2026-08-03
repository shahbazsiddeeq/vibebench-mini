def parse_config(path):
    """
    Parse an INI-style configuration file.
    
    Args:
        path: Path to the configuration file
        
    Returns:
        Dictionary mapping section names to dictionaries of key-value pairs
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If duplicate sections are found
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    
    result = {}
    current_section = None
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        
        # Skip blank lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Check if it's a section header
        if line.startswith('[') and line.endswith(']'):
            section_name = line[1:-1]
            
            # Check for duplicate section
            if section_name in result:
                raise ValueError(f"Duplicate section: {section_name}")
            
            current_section = section_name
            result[current_section] = {}
        
        # Otherwise, it should be a key=value pair
        elif '=' in line:
            if current_section is None:
                # Key-value pair before any section header
                continue
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            result[current_section][key] = value
    
    return result
