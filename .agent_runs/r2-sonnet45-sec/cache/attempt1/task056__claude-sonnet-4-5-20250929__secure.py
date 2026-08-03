import os
import re


def parse_config(path):
    """
    Parse an INI-style configuration file.
    
    Args:
        path: Path to the configuration file
        
    Returns:
        Dictionary mapping section names to dictionaries of key-value pairs
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If duplicate sections are found or invalid format
    """
    # Validate input path
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")
    
    result = {}
    current_section = None
    seen_sections = set()
    
    # Read file securely
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Strip whitespace
                line = line.strip()
                
                # Skip blank lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Check for section header
                section_match = re.match(r'^\[([^\]]+)\]$', line)
                if section_match:
                    section_name = section_match.group(1).strip()
                    
                    # Check for duplicate sections
                    if section_name in seen_sections:
                        raise ValueError(f"Duplicate section: {section_name}")
                    
                    seen_sections.add(section_name)
                    current_section = section_name
                    result[current_section] = {}
                    continue
                
                # Check for key=value pair
                if '=' in line:
                    # Split on first '=' only
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    
                    # Validate we're in a section
                    if current_section is None:
                        raise ValueError(f"Key-value pair found outside of section at line {line_num}")
                    
                    # Validate key is not empty
                    if not key:
                        raise ValueError(f"Empty key at line {line_num}")
                    
                    # Store the key-value pair
                    result[current_section][key] = value
                else:
                    # Line is neither a section, comment, blank, nor key=value
                    raise ValueError(f"Invalid line format at line {line_num}: {line}")
    
    except UnicodeDecodeError:
        raise ValueError("File contains invalid UTF-8 encoding")
    except OSError as e:
        raise ValueError(f"Error reading file: {e}")
    
    return result
