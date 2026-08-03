# src/solution.py

def parse_config(path):
    import os

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: '{path}'")

    config = {}
    current_section = None

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1].strip()
                if section in config:
                    raise ValueError(f"Duplicate section: '{section}'")
                config[section] = {}
                current_section = section
            else:
                if current_section is None:
                    raise ValueError("Key-value pair outside of a section")
                if '=' not in line:
                    raise ValueError(f"Invalid line: '{line}'")
                key, value = line.split('=', 1)
                config[current_section][key.strip()] = value.strip()

    return config
