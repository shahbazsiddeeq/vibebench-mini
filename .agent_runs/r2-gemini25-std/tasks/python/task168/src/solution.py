def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """
    Parses an HTTP Content-Type (or media-type) header value into (media_type, params).

    The value is split into ';'-separated fields, but ';' characters INSIDE a
    double-quoted string do NOT split (quoted strings are honored).
    The FIRST field is the media type: it is stripped of surrounding whitespace
    and LOWERCASED, and must be 'type/subtype' with exactly one '/' and non-empty
    type and subtype (else ValueError).
    Each remaining field is a parameter 'name=value': the name is stripped and
    LOWERCASED; the value is stripped and, if it begins with '\"', is treated
    as an RFC-2616 quoted-string (surrounding double quotes removed and backslash
    escapes '\\\\x' -> 'x' unescaped) otherwise taken verbatim (an unquoted token
    value keeps its original case).
    Empty fields produced by doubled or trailing ';' are skipped.
    A parameter field with no '=' raises ValueError.
    Duplicate parameter names: the LAST occurrence wins.
    Parameter values keep their case; only the media type and parameter NAMES
    are lowercased.
    Return type is tuple[str, dict[str, str]] (empty dict when there are no parameters).
    """

    fields = []
    in_quote = False
    start = 0
    for i, char in enumerate(value):
        if char == '"':
            in_quote = not in_quote
        elif char == ';' and not in_quote:
            field = value[start:i].strip()
            if field:
                fields.append(field)
            start = i + 1
    field = value[start:].strip()
    if field:
        fields.append(field)

    if not fields:
        raise ValueError("Empty Content-Type header")

    media_type_str = fields[0].lower()
    if '/' not in media_type_str:
        raise ValueError("Media type must contain a '/'")
    parts = media_type_str.split('/')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Media type must be 'type/subtype' with non-empty type and subtype")

    params = {}
    for field in fields[1:]:
        if '=' not in field:
            raise ValueError(f"Parameter field '{field}' has no '='")
        name, val = field.split('=', 1)
        name = name.strip().lower()
        val = val.strip()

        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
            # Unescape quoted string: \\x -> x
            unescaped_val = []
            i = 0
            while i < len(val):
                if val[i] == '\\' and i + 1 < len(val):
                    unescaped_val.append(val[i+1])
                    i += 2
                else:
                    unescaped_val.append(val[i])
                    i += 1
            val = "".join(unescaped_val)
        
        params[name] = val

    return media_type_str, params
