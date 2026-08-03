# src/solution.py

def parse_config(path):
    config = {}
    
    try:
        with open(path, 'r') as file:
            current_section = None
            
            for line in file:
                line = line.strip()
                
                # Ignore comments and blank lines
                if not line or line.startswith('#'):
                    continue
                
                # Check for section headers
                if line.startswith('[') and line.endswith(']'):
                    section_name = line[1:-1].strip()
                    if section_name in config:
                        raise ValueError(f"Duplicate section: {section_name}")
                    current_section = section_name
                    config[current_section] = {}
                elif '=' in line and current_section is not None:
                    key, value = line.split('=', 1)
                    config[current_section][key.strip()] = value.strip()
                else:
                    raise ValueError(f"Invalid line: {line}")
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    return config
