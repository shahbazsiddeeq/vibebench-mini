# src/solution.py

import os

def write_config(path, config):
    # Validate the path
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid path provided.")
    
    # Validate the config
    if not isinstance(config, dict):
        raise ValueError("Config must be a dictionary.")
    
    # Prepare the content for the INI file
    lines = []
    
    for section, values in config.items():
        if not isinstance(section, str) or not section.strip():
            raise ValueError("Section names must be non-empty strings.")
        if not isinstance(values, dict):
            raise ValueError("Section values must be dictionaries.")
        
        # Add section header
        lines.append(f"[{section}]")
        
        for key, value in values.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Keys must be non-empty strings.")
            if not isinstance(value, str):
                raise ValueError("Values must be strings.")
            if '\n' in value or '\r' in value:
                raise ValueError("Values must not contain line breaks.")
            
            # Add key-value pair
            lines.append(f"{key}={value}")
        
        # Add a blank line after each section
        lines.append("")
    
    # Join all lines into a single string
    content = "\n".join(lines).strip()  # Strip to remove the last blank line if needed

    # Write to the file with UTF-8 encoding
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
