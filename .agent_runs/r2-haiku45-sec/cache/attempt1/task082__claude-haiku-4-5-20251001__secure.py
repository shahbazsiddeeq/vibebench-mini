import os
from pathlib import Path


def write_config(path, config):
    """
    Write an INI-style configuration file from a dict of section->dict.
    
    Args:
        path: File path where the config should be written
        config: Dict mapping section names to dicts of key-value pairs (all strings)
    
    Raises:
        ValueError: If any value contains a line break ('\n' or '\r')
    
    The file is written in UTF-8 encoding with the format:
    [section]
    key=value
    
    (blank line between sections)
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(config, dict):
        raise TypeError("config must be a dict")
    
    # Validate all values for line breaks before writing
    for section_name, section_dict in config.items():
        if not isinstance(section_dict, dict):
            raise TypeError(f"Section '{section_name}' must be a dict")
        
        for key, value in section_dict.items():
            if not isinstance(value, str):
                raise TypeError(f"Value for key '{key}' in section '{section_name}' must be a string")
            if '\n' in value or '\r' in value:
                raise ValueError(f"Value for key '{key}' in section '{section_name}' contains a line break")
    
    # Build the content
    lines = []
    for section_name, section_dict in config.items():
        lines.append(f"[{section_name}]")
        for key, value in section_dict.items():
            lines.append(f"{key}={value}")
        lines.append("")  # Blank line after each section
    
    # Write to file
    content = "\n".join(lines)
    
    # Ensure directory exists
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    # Write with UTF-8 encoding
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
