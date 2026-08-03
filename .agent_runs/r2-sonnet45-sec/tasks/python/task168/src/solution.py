def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """
    Parse an HTTP Content-Type header value into (media_type, params).
    
    Args:
        value: The Content-Type header value string
        
    Returns:
        A tuple of (media_type, params_dict)
        
    Raises:
        ValueError: If media type format is invalid or parameter has no '='
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    
    # Split by semicolons, but respect quoted strings
    fields = _split_respecting_quotes(value)
    
    if not fields:
        raise ValueError("Empty content type")
    
    # First field is the media type
    media_type = fields[0].strip().lower()
    
    # Validate media type format: must be type/subtype
    if '/' not in media_type:
        raise ValueError("Media type must contain '/'")
    
    parts = media_type.split('/')
    if len(parts) != 2:
        raise ValueError("Media type must have exactly one '/'")
    
    type_part, subtype_part = parts
    if not type_part or not subtype_part:
        raise ValueError("Media type and subtype must be non-empty")
    
    # Parse parameters from remaining fields
    params = {}
    for field in fields[1:]:
        field = field.strip()
        if not field:  # Skip empty fields
            continue
            
        if '=' not in field:
            raise ValueError(f"Parameter field must contain '=': {field}")
        
        # Split on first '=' only
        name, value = field.split('=', 1)
        name = name.strip().lower()
        value = value.strip()
        
        # Handle quoted strings
        if value.startswith('"'):
            value = _unquote_string(value)
        
        # Last occurrence wins for duplicate names
        params[name] = value
    
    return (media_type, params)


def _split_respecting_quotes(value: str) -> list[str]:
    """
    Split a string by semicolons, but not semicolons inside quoted strings.
    """
    fields = []
    current_field = []
    in_quotes = False
    escaped = False
    
    for char in value:
        if escaped:
            current_field.append(char)
            escaped = False
        elif char == '\\' and in_quotes:
            current_field.append(char)
            escaped = True
        elif char == '"':
            current_field.append(char)
            in_quotes = not in_quotes
        elif char == ';' and not in_quotes:
            fields.append(''.join(current_field))
            current_field = []
        else:
            current_field.append(char)
    
    # Add the last field
    if current_field or fields:  # Don't add empty if input was empty
        fields.append(''.join(current_field))
    
    return fields


def _unquote_string(value: str) -> str:
    """
    Remove surrounding quotes and unescape backslash sequences in a quoted string.
    Follows RFC 2616 quoted-string rules.
    """
    if not value.startswith('"'):
        return value
    
    # Remove surrounding quotes
    if len(value) >= 2 and value.endswith('"'):
        value = value[1:-1]
    else:
        # Malformed, but be lenient - just remove leading quote
        value = value[1:]
    
    # Unescape: \x -> x
    result = []
    escaped = False
    for char in value:
        if escaped:
            result.append(char)
            escaped = False
        elif char == '\\':
            escaped = True
        else:
            result.append(char)
    
    return ''.join(result)
