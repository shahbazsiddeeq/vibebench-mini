import os
from pathlib import Path


def write_config(path, config):
    """
    Write an INI-style configuration file from a dictionary.
    
    Args:
        path: File path to write to (string or Path-like)
        config: Dictionary mapping section names to dictionaries of key-value pairs
        
    Raises:
        ValueError: If any value contains a line break (\n or \r)
    """
    # Validate inputs
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    
    # Validate all values before writing anything
    for section_name, section_dict in config.items():
        if not isinstance(section_dict, dict):
            raise TypeError(f"Section '{section_name}' must be a dictionary")
        
        for key, value in section_dict.items():
            # Convert to string if not already
            value_str = str(value)
            
            # Check for line breaks
            if '\n' in value_str or '\r' in value_str:
                raise ValueError(f"Value for key '{key}' in section '{section_name}' contains a line break")
    
    # Build the content
    lines = []
    
    for section_name, section_dict in config.items():
        # Write section header
        lines.append(f"[{section_name}]")
        
        # Write key-value pairs
        for key, value in section_dict.items():
            lines.append(f"{key}={value}")
        
        # Add blank line after section
        lines.append("")
    
    # Join all lines with newline
    content = "\n".join(lines)
    
    # Write to file with UTF-8 encoding
    # Use Path for safer file handling
    file_path = Path(path)
    
    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the file
    file_path.write_text(content, encoding='utf-8')
