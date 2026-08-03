import re

def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    # Split the value into parts, respecting quoted strings
    parts = []
    current_part = []
    in_quotes = False

    for char in value:
        if char == '"':
            in_quotes = not in_quotes
        if char == ';' and not in_quotes:
            parts.append(''.join(current_part).strip())
            current_part = []
        else:
            current_part.append(char)

    # Add the last part
    if current_part:
        parts.append(''.join(current_part).strip())

    # Validate and process the media type
    media_type = parts[0].strip().lower()
    if '/' not in media_type or media_type.count('/') != 1:
        raise ValueError("Invalid media type format")
    
    # Prepare the parameters dictionary
    params = {}
    
    for part in parts[1:]:
        if '=' not in part:
            raise ValueError("Parameter must contain '='")
        
        name, value = part.split('=', 1)
        name = name.strip().lower()
        value = value.strip()

        # Handle quoted values
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace(r'\\', '\\').replace(r'\"', '"')
        
        # Store the parameter
        params[name] = value

    return media_type, params
