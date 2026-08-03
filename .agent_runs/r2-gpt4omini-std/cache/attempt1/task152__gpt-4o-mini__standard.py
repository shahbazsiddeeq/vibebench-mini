import os
import re

def parse_dotenv(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist.")
    
    result = {}
    key_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('export '):
                line = line[7:]  # Remove 'export ' prefix
            
            if '=' not in line:
                raise ValueError(f"Line does not contain '=': {line}")
            
            key, raw_value = line.split('=', 1)
            key = key.strip()
            if not key or not key_pattern.match(key):
                raise ValueError(f"Invalid key: {key}")
            
            if raw_value.startswith('"') and raw_value.endswith('"'):
                value = raw_value[1:-1].encode().decode('unicode_escape')
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                value = raw_value[1:-1]
            else:
                value = raw_value.split('#', 1)[0].rstrip()
            
            result[key] = value

    return result
