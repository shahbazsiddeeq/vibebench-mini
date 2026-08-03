def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """Parse an HTTP Content-Type header value into (media_type, params)."""
    
    # Split by semicolons, but respect quoted strings
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    
    while i < len(value):
        char = value[i]
        
        if char == '\\' and in_quotes and i + 1 < len(value):
            # Escaped character in quoted string - add both backslash and next char
            current_field.append(char)
            current_field.append(value[i + 1])
            i += 2
            continue
        elif char == '"':
            in_quotes = not in_quotes
            current_field.append(char)
            i += 1
        elif char == ';' and not in_quotes:
            # Field separator
            fields.append(''.join(current_field))
            current_field = []
            i += 1
        else:
            current_field.append(char)
            i += 1
    
    # Don't forget the last field
    if current_field:
        fields.append(''.join(current_field))
    
    # First field is the media type
    if not fields:
        raise ValueError("Empty content type")
    
    media_type = fields[0].strip().lower()
    
    # Validate media type format: type/subtype
    if '/' not in media_type:
        raise ValueError("Media type must contain '/'")
    
    parts = media_type.split('/')
    if len(parts) != 2:
        raise ValueError("Media type must have exactly one '/'")
    
    type_part, subtype_part = parts
    if not type_part or not subtype_part:
        raise ValueError("Media type and subtype must be non-empty")
    
    # Parse parameters
    params = {}
    for field in fields[1:]:
        field = field.strip()
        if not field:
            # Skip empty fields
            continue
        
        if '=' not in field:
            raise ValueError(f"Parameter field must contain '=': {field}")
        
        # Split on first '=' only
        name, value = field.split('=', 1)
        name = name.strip().lower()
        value = value.strip()
        
        # Handle quoted values
        if value.startswith('"'):
            # Quoted string - remove quotes and unescape
            if not value.endswith('"') or len(value) < 2:
                # Malformed quoted string, but let's be lenient
                # Actually, let's handle the case where it starts with " but doesn't end with "
                if len(value) >= 2 and value.endswith('"'):
                    value = value[1:-1]
                else:
                    # Just remove the leading quote
                    value = value[1:]
            else:
                value = value[1:-1]
            
            # Unescape backslash sequences
            unescaped = []
            i = 0
            while i < len(value):
                if value[i] == '\\' and i + 1 < len(value):
                    # Escaped character - take the next character literally
                    unescaped.append(value[i + 1])
                    i += 2
                else:
                    unescaped.append(value[i])
                    i += 1
            value = ''.join(unescaped)
        
        # Last occurrence wins
        params[name] = value
    
    return (media_type, params)
