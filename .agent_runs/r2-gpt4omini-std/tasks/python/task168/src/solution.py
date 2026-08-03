def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
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

    if not parts or len(parts) < 1:
        raise ValueError("Invalid Content-Type header")

    media_type = parts[0].strip().lower()
    if '/' not in media_type or media_type.count('/') != 1:
        raise ValueError("Invalid media type format")

    params = {}
    for part in parts[1:]:
        if not part:
            continue
        if '=' not in part:
            raise ValueError("Parameter must contain '='")
        
        name_value = part.split('=', 1)
        name = name_value[0].strip().lower()
        value = name_value[1].strip()

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        
        params[name] = value

    return media_type, params
