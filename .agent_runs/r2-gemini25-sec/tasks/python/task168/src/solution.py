def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """
    Parses an HTTP Content-Type (or media-type) header value into (media_type, params).

    The value is split into ';'-separated fields, but ';' characters INSIDE a
    double-quoted string do NOT split (quoted strings are honored). The FIRST
    field is the media type: it is stripped of surrounding whitespace and
    LOWERCASED, and must be 'type/subtype' with exactly one '/' and non-empty
    type and subtype (else ValueError). Each remaining field is a parameter
    'name=value': the name is stripped and LOWERCASED; the value is stripped
    and, if it begins with '"', is treated as an RFC-2616 quoted-string
    (surrounding double quotes removed and backslash escapes '\\x' -> 'x'
    unescaped) otherwise taken verbatim (an unquoted token value keeps its
    original case). Empty fields produced by doubled or trailing ';' are
    skipped. A parameter field with no '=' raises ValueError. Duplicate
    parameter names: the LAST occurrence wins. Parameter values keep their case;
    only the media type and parameter NAMES are lowercased.
    Return type is tuple[str, dict[str, str]] (empty dict when there are no
    parameters).

    Args:
        value: The Content-Type header string.

    Returns:
        A tuple containing the lowercased media type string and a dictionary
        of lowercased parameter names to their string values.

    Raises:
        ValueError: If the media type is invalid or a parameter field is malformed.
        TypeError: If the input value is not a string.
    """
    if not isinstance(value, str):
        raise TypeError("Input 'value' must be a string.")

    fields = _split_on_semicolon_respecting_quotes(value)
    if not fields:
        raise ValueError("Content-Type header cannot be empty.")

    media_type_str = fields[0].strip()
    if not media_type_str:
        raise ValueError("Media type cannot be empty.")

    media_type_parts = media_type_str.split('/')
    if len(media_type_parts) != 2 or not media_type_parts[0] or not media_type_parts[1]:
        raise ValueError(f"Invalid media type format: '{media_type_str}'")
    media_type = media_type_str.lower()

    params: dict[str, str] = {}
    for field in fields[1:]:
        field = field.strip()
        if not field:
            continue

        if '=' not in field:
            raise ValueError(f"Malformed parameter field (missing '='): '{field}'")

        name_part, value_part = field.split('=', 1)
        name = name_part.strip().lower()
        value = value_part.strip()

        if not name:
            raise ValueError(f"Parameter name cannot be empty: '{field}'")

        if value.startswith('"') and value.endswith('"'):
            # RFC 2616 quoted-string parsing
            value = value[1:-1]  # Remove surrounding quotes
            # Unescape backslash-escaped characters
            unescaped_value = []
            i = 0
            while i < len(value):
                if value[i] == '\\' and i + 1 < len(value):
                    unescaped_value.append(value[i+1])
                    i += 2
                else:
                    unescaped_value.append(value[i])
                    i += 1
            value = "".join(unescaped_value)
        # Else, unquoted token value, keep original case and don't unescape

        params[name] = value

    return media_type, params


def _split_on_semicolon_respecting_quotes(s: str) -> list[str]:
    """
    Splits a string by semicolons, respecting double-quoted substrings.
    Semicolons inside double quotes do not cause a split.
    """
    parts = []
    current_part = []
    in_quote = False
    i = 0
    while i < len(s):
        char = s[i]
        if char == '"':
            in_quote = not in_quote
            current_part.append(char)
        elif char == ';' and not in_quote:
            parts.append("".join(current_part))
            current_part = []
        else:
            current_part.append(char)
        i += 1
    parts.append("".join(current_part))
    return parts
