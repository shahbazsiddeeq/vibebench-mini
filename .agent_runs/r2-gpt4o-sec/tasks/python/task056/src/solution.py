import os

def parse_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    config = {}
    current_section = None

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1].strip()
                if section in config:
                    raise ValueError(f"Duplicate section: {section}")
                config[section] = {}
                current_section = section
            elif '=' in line and current_section is not None:
                key, value = map(str.strip, line.split('=', 1))
                config[current_section][key] = value
            else:
                raise ValueError(f"Invalid line: {line}")

    return config
