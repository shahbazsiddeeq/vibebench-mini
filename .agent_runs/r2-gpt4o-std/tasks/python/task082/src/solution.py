def write_config(path, config):
    with open(path, 'w', encoding='utf-8') as file:
        for section, pairs in config.items():
            file.write(f"[{section}]\n")
            for key, value in pairs.items():
                if '\n' in value or '\r' in value:
                    raise ValueError("Value contains a line break")
                file.write(f"{key}={value}\n")
            file.write("\n")
