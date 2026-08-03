def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """
    Parse an HTTP Content-Type header value into (media_type, params).
    
    The value is split into ';'-separated fields, but ';' characters inside
    double-quoted strings are honored (not treated as separators).
    
    The FIRST field is the media type: stripped of whitespace, lowercased,
    and must be 'type/subtype' with exactly one '/' and non-empty parts.
    
    Each remaining field is a parameter 'name=value':
    - name: stripped and lowercased
    - value: stripped; if starts with '"', treated as RFC-2616 quoted-string
             (surrounding quotes removed, backslash escapes unescaped);
             otherwise taken verbatim with case preserved
    
    Empty fields from doubled or trailing ';' are skipped.
    Duplicate parameter names: last occurrence wins.
    """
    
    # Split by ';' while respecting quoted strings
    fields = _split_by_semicolon(value)
    
    if not fields:
        raise ValueError("Empty content-type")
    
    # Parse media type (first field)
    media_type = fields[0].strip().lower()
    
    # Validate media type format
    if '/' not in media_type:
        raise ValueError("Media type must contain '/'")
    
    parts = media_type.split('/')
    if len(parts) != 2:
        raise ValueError("Media type must have exactly one '/'")
    
    type_part, subtype_part = parts
    if not type_part or not subtype_part:
        raise ValueError("Media type must have non-empty type and subtype")
    
    # Parse parameters
    params = {}
    for field in fields[1:]:
        field = field.strip()
        if not field:  # Skip empty fields
            continue
        
        if '=' not in field:
            raise ValueError(f"Parameter field must contain '=': {field}")
        
        name, value = field.split('=', 1)
        name = name.strip().lower()
        value = value.strip()
        
        # Handle quoted values
        if value.startswith('"'):
            if not value.endswith('"'):
                raise ValueError(f"Quoted value not properly closed: {value}")
            # Remove surrounding quotes and unescape
            value = _unescape_quoted_string(value[1:-1])
        
        params[name] = value
    
    return (media_type, params)


def _split_by_semicolon(value: str) -> list[str]:
    """
    Split a string by ';' while respecting double-quoted strings.
    Characters inside quoted strings are not treated as separators.
    """
    fields = []
    current = []
    in_quotes = False
    i = 0
    
    while i < len(value):
        char = value[i]
        
        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
        elif char == ';' and not in_quotes:
            fields.append(''.join(current))
            current = []
        else:
            current.append(char)
        
        i += 1
    
    # Add the last field
    fields.append(''.join(current))
    
    return fields


def _unescape_quoted_string(quoted_value: str) -> str:
    """
    Unescape an RFC-2616 quoted-string.
    Backslash escapes are converted: '\\x' -> 'x'
    """
    result = []
    i = 0
    
    while i < len(quoted_value):
        if quoted_value[i] == '\\' and i + 1 < len(quoted_value):
            # Skip the backslash and take the next character
            result.append(quoted_value[i + 1])
            i += 2
        else:
            result.append(quoted_value[i])
            i += 1
    
    return ''.join(result)
