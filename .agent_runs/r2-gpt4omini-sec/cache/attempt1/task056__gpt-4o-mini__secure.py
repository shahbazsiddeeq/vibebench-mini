# src/solution.py

import os

def parse_config(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    
    config = {}
    current_section = None

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Ignore blank lines and comments
            
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1].strip()
                if section_name in config:
                    raise ValueError(f"Duplicate section found: '{section_name}'")
                current_section = section_name
                config[current_section] = {}
            elif '=' in line and current_section is not None:
                key, value = line.split('=', 1)
                config[current_section][key.strip()] = value.strip()
            else:
                raise ValueError(f"Invalid line format: '{line}'")

    return config
