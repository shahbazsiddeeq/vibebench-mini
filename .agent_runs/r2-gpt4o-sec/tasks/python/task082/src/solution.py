import os

def write_config(path, config):
    if not isinstance(config, dict):
        raise ValueError("Config must be a dictionary.")

    with open(path, 'w', encoding='utf-8') as file:
        for section, pairs in config.items():
            if not isinstance(section, str) or not isinstance(pairs, dict):
                raise ValueError("Invalid section or key-value pairs.")
            
            file.write(f"[{section}]\n")
            for key, value in pairs.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ValueError("Keys and values must be strings.")
                if '\n' in value or '\r' in value:
                    raise ValueError("Values cannot contain line breaks.")
                
                file.write(f"{key}={value}\n")
            file.write("\n")
