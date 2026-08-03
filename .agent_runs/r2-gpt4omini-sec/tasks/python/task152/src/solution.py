# src/solution.py

import os
import re

def parse_dotenv(path: str) -> dict[str, str]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
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
                raise ValueError(f"Invalid line (no '=' found): {line}")
            
            key, raw_value = line.split('=', 1)
            key = key.strip()
            if not key or not key_pattern.match(key):
                raise ValueError(f"Invalid key: {key}")
            
            # Process the value
            if raw_value.startswith('"') and raw_value.endswith('"'):
                # Double-quoted value
                value = raw_value[1:-1].replace(r'\\', '\\').replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\r', '\r').replace(r'\"', '"')
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                # Single-quoted value
                value = raw_value[1:-1]
            else:
                # Unquoted value
                comment_index = raw_value.find('#')
                if comment_index != -1:
                    raw_value = raw_value[:comment_index]
                value = raw_value.strip()
            
            result[key] = value
    
    return result
