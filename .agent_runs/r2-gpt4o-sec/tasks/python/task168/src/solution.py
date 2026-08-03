import re

def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    # Regular expression to match a quoted string
    quoted_string_re = re.compile(r'"((?:[^"\\]|\\.)*)"')

    # Split the input into parts, respecting quoted strings
    parts = []
    pos = 0
    while pos < len(value):
        if value[pos] == '"':
            match = quoted_string_re.match(value, pos)
            if not match:
                raise ValueError("Invalid quoted string")
            parts.append(match.group(0))
            pos = match.end()
        else:
            next_pos = value.find(';', pos)
            if next_pos == -1:
                parts.append(value[pos:])
                break
            parts.append(value[pos:next_pos])
            pos = next_pos + 1

    # Process the media type
    media_type = parts[0].strip().lower()
    if media_type.count('/') != 1:
        raise ValueError("Invalid media type format")
    type_part, subtype_part = media_type.split('/')
    if not type_part or not subtype_part:
        raise ValueError("Type and subtype must be non-empty")

    # Process parameters
    params = {}
    for part in parts[1:]:
        part = part.strip()
        if not part:
            continue
        if '=' not in part:
            raise ValueError("Parameter must contain '='")
        name, value = part.split('=', 1)
        name = name.strip().lower()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            value = re.sub(r'\\(.)', r'\1', value)
        params[name] = value

    return media_type, params
