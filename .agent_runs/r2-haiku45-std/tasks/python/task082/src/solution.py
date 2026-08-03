def write_config(path, config):
    """
    Write an INI-style configuration file from a dict of section->dict.
    
    Args:
        path: File path to write to
        config: Dict mapping section names to dicts of key-value pairs
        
    Raises:
        ValueError: If any value contains a line break ('\n' or '\r')
    """
    # Validate that no values contain line breaks
    for section, pairs in config.items():
        for key, value in pairs.items():
            if '\n' in value or '\r' in value:
                raise ValueError(f"Value contains line break: {value}")
    
    # Build the content
    lines = []
    for section, pairs in config.items():
        lines.append(f"[{section}]")
        for key, value in pairs.items():
            lines.append(f"{key}={value}")
        lines.append("")  # Blank line after each section
    
    # Write to file with UTF-8 encoding
    content = "\n".join(lines)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
