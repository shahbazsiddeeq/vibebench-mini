import re
from typing import Dict


def parse_dotenv(path: str) -> Dict[str, str]:
    """Parse a .env file into a dictionary."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    result = {}
    
    for line in lines:
        # Strip the line
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Remove optional leading 'export ' prefix
        if line.startswith('export '):
            line = line[7:]
        
        # Split on the FIRST '='
        if '=' not in line:
            raise ValueError(f"No '=' found in line: {line}")
        
        key, raw_value = line.split('=', 1)
        
        # Strip and validate key
        key = key.strip()
        if not key:
            raise ValueError("Key is empty")
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
            raise ValueError(f"Invalid key: {key}")
        
        # Parse the value
        value = parse_value(raw_value)
        
        result[key] = value
    
    return result


def parse_value(raw_value: str) -> str:
    """Parse the value according to the rules."""
    # Check for double-quoted value
    if raw_value.startswith('"') and raw_value.endswith('"'):
        # Remove quotes and unescape
        content = raw_value[1:-1]
        content = content.replace('\\n', '\n')
        content = content.replace('\\t', '\t')
        content = content.replace('\\r', '\r')
        content = content.replace('\\\\', '\\')
        content = content.replace('\\"', '"')
        return content
    
    # Check for single-quoted value
    if raw_value.startswith("'") and raw_value.endswith("'"):
        # Remove quotes and take literally
        return raw_value[1:-1]
    
    # Unquoted value: strip inline comments and whitespace
    # Inline comment is '#' at index 0 or immediately preceded by whitespace
    value = raw_value
    
    # Find inline comment
    i = 0
    while i < len(value):
        if value[i] == '#':
            # Check if it's at index 0 or preceded by whitespace
            if i == 0 or value[i-1].isspace():
                value = value[:i]
                break
        i += 1
    
    # Strip surrounding whitespace
    value = value.strip()
    
    return value
