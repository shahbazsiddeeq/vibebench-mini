def parse_config(path):
    """
    Parse an INI-style config file.
    
    Args:
        path: Path to the config file
        
    Returns:
        dict: Dictionary mapping section names to dictionaries of key-value pairs
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If duplicate sections are found
    """
    result = {}
    current_section = None
    
    with open(path, 'r') as f:
        for line in f:
            # Strip whitespace
            line = line.strip()
            
            # Skip blank lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Check for section header
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1]
                
                # Check for duplicate sections
                if section_name in result:
                    raise ValueError(f"Duplicate section: {section_name}")
                
                current_section = section_name
                result[current_section] = {}
            else:
                # Parse key=value pair
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if current_section is not None:
                        result[current_section][key] = value
    
    return result
