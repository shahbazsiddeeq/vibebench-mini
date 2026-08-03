def parse_config(path):
    """
    Parses an INI-style configuration file.

    Args:
        path (str): The path to the configuration file.

    Returns:
        dict: A dictionary where keys are section names and values are
              dictionaries of key-value pairs within that section.

    Raises:
        FileNotFoundError: If the file specified by 'path' does not exist.
        ValueError: If a duplicate section is found in the configuration file.
    """
    config = {}
    current_section = None

    try:
        with open(path, 'r') as f:
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
                    current_section = section_name
                elif '=' in line:
                    if current_section is None:
                        raise ValueError(f"Key-value pair found outside any section on line {line_num} in {path}")
                    
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if not key:
                        raise ValueError(f"Invalid empty key on line {line_num} in section '{current_section}' in {path}")

                    config[current_section][key] = value
                else:
                    raise ValueError(f"Invalid line format on line {line_num} in {path}: '{line}'")
    except FileNotFoundError:
        raise
    except Exception as e:
        # Catch other potential file reading errors or parsing errors
        raise ValueError(f"Error parsing config file '{path}': {e}") from e

    return config
