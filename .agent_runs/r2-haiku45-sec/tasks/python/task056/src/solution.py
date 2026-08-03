import re
from pathlib import Path


def parse_config(path: str) -> dict:
    """
    Parse an INI-style configuration file.
    
    Args:
        path: Path to the configuration file
        
    Returns:
        Dictionary mapping section names to dictionaries of key-value pairs
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If duplicate sections are found
    """
    # Validate input
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    # Convert to Path object for safe file handling
    file_path = Path(path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    # Read file safely
    try:
        content = file_path.read_text(encoding='utf-8')
    except (IOError, OSError) as e:
        raise FileNotFoundError(f"Cannot read configuration file: {path}") from e
    
    result = {}
    current_section = None
    
    # Process each line
    for line_num, line in enumerate(content.splitlines(), 1):
        # Strip whitespace
        stripped = line.strip()
        
        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue
        
        # Check for section header
        section_match = re.match(r'^\[([^\]]+)\]$', stripped)
        if section_match:
            section_name = section_match.group(1).strip()
            
            # Validate section name is not empty
            if not section_name:
                raise ValueError(f"Empty section name at line {line_num}")
            
            # Check for duplicate sections
            if section_name in result:
                raise ValueError(f"Duplicate section: [{section_name}]")
            
            current_section = section_name
            result[current_section] = {}
            continue
        
        # Check for key=value pair
        if '=' in stripped:
            if current_section is None:
                raise ValueError(f"Key-value pair found before any section at line {line_num}")
            
            # Split on first '=' only
            key, _, value = stripped.partition('=')
            key = key.strip()
            value = value.strip()
            
            # Validate key is not empty
            if not key:
                raise ValueError(f"Empty key at line {line_num}")
            
            # Store the key-value pair
            result[current_section][key] = value
            continue
        
        # If we get here, it's an invalid line
        if stripped and not stripped.startswith('#'):
            raise ValueError(f"Invalid line format at line {line_num}: {stripped}")
    
    return result
