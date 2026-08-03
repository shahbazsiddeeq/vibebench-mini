import re
from typing import Tuple, Dict


def parse_content_type(value: str) -> Tuple[str, Dict[str, str]]:
    """
    Parse an HTTP Content-Type header value into (media_type, params).
    
    The value is split into ';'-separated fields, but ';' characters inside
    double-quoted strings are preserved. The first field is the media type
    (lowercased, must be 'type/subtype'). Remaining fields are parameters
    'name=value' where names are lowercased and values may be quoted strings.
    
    Args:
        value: The Content-Type header value string
        
    Returns:
        A tuple of (media_type, params_dict)
        
    Raises:
        ValueError: If media type is invalid or parameter format is wrong
    """
    if not isinstance(value, str):
        raise ValueError("Content-Type value must be a string")
    
    # Split by semicolon while respecting quoted strings
    fields = _split_by_semicolon(value)
    
    if not fields:
        raise ValueError("Content-Type value cannot be empty")
    
    # Parse media type (first field)
    media_type_str = fields[0].strip()
    if not media_type_str:
        raise ValueError("Media type cannot be empty")
    
    media_type = _parse_media_type(media_type_str)
    
    # Parse parameters (remaining fields)
    params: Dict[str, str] = {}
    for field in fields[1:]:
        field = field.strip()
        if not field:  # Skip empty fields from doubled or trailing semicolons
            continue
        
        if '=' not in field:
            raise ValueError(f"Parameter field must contain '=': {field}")
        
        name, value = field.split('=', 1)
        name = name.strip().lower()
        value = value.strip()
        
        if not name:
            raise ValueError("Parameter name cannot be empty")
        
        # Parse the value (handle quoted strings)
        parsed_value = _parse_parameter_value(value)
        params[name] = parsed_value
    
    return (media_type, params)


def _split_by_semicolon(value: str) -> list:
    """
    Split a string by semicolons, but preserve semicolons inside quoted strings.
    """
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    
    while i < len(value):
        char = value[i]
        
        if char == '"':
            # Toggle quote state
            in_quotes = not in_quotes
            current_field.append(char)
        elif char == ';' and not in_quotes:
            # Found a field separator
            fields.append(''.join(current_field))
            current_field = []
        else:
            current_field.append(char)
        
        i += 1
    
    # Add the last field
    if current_field or (value and value[-1] == ';'):
        fields.append(''.join(current_field))
    
    return fields


def _parse_media_type(media_type_str: str) -> str:
    """
    Parse and validate the media type (type/subtype format).
    Returns the lowercased media type.
    """
    media_type_str = media_type_str.lower()
    
    if '/' not in media_type_str:
        raise ValueError(f"Media type must contain '/': {media_type_str}")
    
    parts = media_type_str.split('/')
    if len(parts) != 2:
        raise ValueError(f"Media type must have exactly one '/': {media_type_str}")
    
    type_part, subtype_part = parts
    
    if not type_part or not subtype_part:
        raise ValueError(f"Media type and subtype must be non-empty: {media_type_str}")
    
    return media_type_str


def _parse_parameter_value(value: str) -> str:
    """
    Parse a parameter value. If it's a quoted string, remove quotes and
    unescape backslash escapes. Otherwise, return as-is.
    """
    if value.startswith('"'):
        # It's a quoted string
        if not value.endswith('"'):
            raise ValueError(f"Quoted value must end with '\"': {value}")
        
        # Remove surrounding quotes
        quoted_content = value[1:-1]
        
        # Unescape backslash escapes: \x -> x
        unescaped = []
        i = 0
        while i < len(quoted_content):
            if quoted_content[i] == '\\' and i + 1 < len(quoted_content):
                # Skip the backslash and take the next character
                unescaped.append(quoted_content[i + 1])
                i += 2
            else:
                unescaped.append(quoted_content[i])
                i += 1
        
        return ''.join(unescaped)
    else:
        # Unquoted token value - keep original case
        return value
