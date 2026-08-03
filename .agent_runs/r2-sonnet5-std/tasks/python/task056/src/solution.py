import os


def parse_config(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: {path}")

    result = {}
    current_section = None

    with open(path, "r") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1].strip()
                if section_name in result:
                    raise ValueError(f"Duplicate section: {section_name}")
                result[section_name] = {}
                current_section = section_name
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if current_section is None:
                    raise ValueError("Key-value pair found before any section header")
                result[current_section][key] = value

    return result
