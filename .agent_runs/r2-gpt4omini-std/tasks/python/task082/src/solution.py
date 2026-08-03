# src/solution.py

def write_config(path, config):
    with open(path, 'w', encoding='utf-8') as f:
        for section, values in config.items():
            if not isinstance(values, dict):
                raise ValueError(f"Values for section '{section}' must be a dictionary.")
            for key, value in values.items():
                if '\n' in value or '\r' in value:
                    raise ValueError(f"Value for key '{key}' in section '{section}' contains a line break.")
            f.write(f"[{section}]\n")
            for key, value in values.items():
                f.write(f"{key}={value}\n")
            f.write("\n")
