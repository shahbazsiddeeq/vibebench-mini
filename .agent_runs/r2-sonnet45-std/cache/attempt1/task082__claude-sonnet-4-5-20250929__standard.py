def write_config(path, config):
    """
    Writes an INI-style configuration file from a dictionary.
    
    Args:
        path: File path to write to
        config: Dict of section name -> dict of key-value pairs
    
    Raises:
        ValueError: If any value contains a line break (\n or \r)
    """
    # Validate that no values contain line breaks
    for section_name, section_dict in config.items():
        for key, value in section_dict.items():
            if '\n' in value or '\r' in value:
                raise ValueError(f"Value contains line break: {value}")
    
    # Build the content
    lines = []
    for section_name, section_dict in config.items():
        lines.append(f"[{section_name}]")
        for key, value in section_dict.items():
            lines.append(f"{key}={value}")
        lines.append("")  # Blank line after each section
    
    # Write to file with UTF-8 encoding
    content = '\n'.join(lines)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
