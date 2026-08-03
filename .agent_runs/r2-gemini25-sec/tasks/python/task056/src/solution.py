import os

def parse_config(path: str) -> dict:
    """
    Parses an INI-style configuration file.

    Args:
        path: The path to the configuration file.

    Returns:
        A dictionary where keys are section names and values are dictionaries
        of key-value pairs within that section.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If a section is duplicated in the configuration file.
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")

    config = {}
    current_section = None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Ignore blank lines and comments
                if not line or line.startswith('#'):
                    continue

                # Section header
                if line.startswith('[') and line.endswith(']'):
                    section_name = line[1:-1].strip()
                    if not section_name:
                        raise ValueError(f"Invalid empty section name on line {line_num} in {path}")
                    if section_name in config:
                        raise ValueError(f"Duplicate section '{section_name}' found on line {line_num} in {path}")
                    config[section_name] = {}
                    current_section = config[section_name]
                elif '=' in line:
                    if current_section is None:
                        raise ValueError(f"Key-value pair found outside any section on line {line_num} in {path}")
                    
                    parts = line.split('=', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()

                    if not key:
                        raise ValueError(f"Invalid empty key on line {line_num} in {path}")
                    
                    # Prevent duplicate keys within the same section
                    if key in current_section:
                        raise ValueError(f"Duplicate key '{key}' in section '{list(config.keys())[-1]}' on line {line_num} in {path}")

                    current_section[key] = value
                else:
                    raise ValueError(f"Malformed line {line_num}: '{line}' in {path}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Error decoding file {path}: {e}") from e
    except IOError as e:
        raise IOError(f"Error reading file {path}: {e}") from e

    return config
