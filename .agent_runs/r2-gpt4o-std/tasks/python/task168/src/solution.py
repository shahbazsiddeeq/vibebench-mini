# src/solution.py

def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    import re

    def unquote(value: str) -> str:
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            return re.sub(r'\\(.)', r'\1', value)
        return value

    parts = []
    current = []
    in_quotes = False

    for char in value:
        if char == ';' and not in_quotes:
            parts.append(''.join(current).strip())
            current = []
        else:
            if char == '"':
                in_quotes = not in_quotes
            current.append(char)

    if current:
        parts.append(''.join(current).strip())

    if not parts:
        raise ValueError("Invalid Content-Type header")

    media_type = parts[0].strip().lower()
    if '/' not in media_type or media_type.count('/') != 1:
        raise ValueError("Invalid media type format")

    type_part, subtype_part = media_type.split('/')
    if not type_part or not subtype_part:
        raise ValueError("Invalid media type format")

    params = {}
    for param in parts[1:]:
        if not param:
            continue
        if '=' not in param:
            raise ValueError("Parameter without '=' found")
        name, value = param.split('=', 1)
        name = name.strip().lower()
        value = unquote(value.strip())
        params[name] = value

    return media_type, params
