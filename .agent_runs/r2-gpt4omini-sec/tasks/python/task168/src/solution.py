# src/solution.py

import re
import secrets

def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    # Validate input
    if not isinstance(value, str):
        raise ValueError("Input must be a string.")
    
    # Split the value into parts, respecting quoted strings
    parts = []
    current_part = []
    in_quotes = False

    for char in value:
        if char == '"':
            in_quotes = not in_quotes
        if char == ';' and not in_quotes:
            if current_part:
                parts.append(''.join(current_part).strip())
                current_part = []
        else:
            current_part.append(char)

    if current_part:
        parts.append(''.join(current_part).strip())

    # Process the media type
    if not parts:
        raise ValueError("Content-Type cannot be empty.")

    media_type = parts[0].strip().lower()
    if '/' not in media_type or media_type.count('/') != 1:
        raise ValueError("Invalid media type format.")

    type_part, subtype_part = media_type.split('/', 1)
    if not type_part or not subtype_part:
        raise ValueError("Invalid media type format.")

    # Process parameters
    params = {}
    for part in parts[1:]:
        if '=' not in part:
            raise ValueError("Parameter must contain '='.")
        
        name, value = part.split('=', 1)
        name = name.strip().lower()
        value = value.strip()

        # Handle quoted values
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace(r'\\', '\\').replace(r'\"', '"')
        
        # Skip empty fields
        if name:
            params[name] = value

    return media_type, params
