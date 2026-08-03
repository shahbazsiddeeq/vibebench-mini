import os
import re

def parse_dotenv(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist")

    result = {}
    key_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Remove 'export ' prefix if present
            if line.startswith('export '):
                line = line[7:]

            # Split on the first '='
            if '=' not in line:
                raise ValueError(f"Invalid line: {line}")
            key, raw_value = line.split('=', 1)

            key = key.strip()
            if not key or not key_pattern.match(key):
                raise ValueError(f"Invalid key: {key}")

            # Process the value
            if raw_value.startswith('"') and raw_value.endswith('"'):
                # Double-quoted value
                value = raw_value[1:-1].encode().decode('unicode_escape')
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                # Single-quoted value
                value = raw_value[1:-1]
            else:
                # Unquoted value
                value = raw_value.split('#', 1)[0].rstrip()
            
            result[key] = value

    return result
