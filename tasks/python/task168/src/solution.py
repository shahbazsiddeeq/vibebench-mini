def _split_fields(value: str) -> list[str]:
    """Split on ';' but never inside a double-quoted string."""
    fields: list[str] = []
    current: list[str] = []
    in_quotes = False
    escaped = False
    for ch in value:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\" and in_quotes:
            current.append(ch)
            escaped = True
            continue
        if ch == '"':
            in_quotes = not in_quotes
            current.append(ch)
            continue
        if ch == ";" and not in_quotes:
            fields.append("".join(current))
            current = []
            continue
        current.append(ch)
    fields.append("".join(current))
    return fields


def _unquote(value: str) -> str:
    """Unescape an RFC-2616 quoted-string that starts with '\"'."""
    if len(value) < 2 or value[-1] != '"':
        raise ValueError(f"unterminated quoted-string: {value!r}")
    inner = value[1:-1]
    result: list[str] = []
    escaped = False
    for ch in inner:
        if escaped:
            result.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        else:
            result.append(ch)
    if escaped:
        raise ValueError(f"dangling escape in quoted-string: {value!r}")
    return "".join(result)


def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """Parse a Content-Type header value into (media_type, params).

    The media type and parameter names are lowercased; parameter values
    keep their case. Quoted-string values are unquoted/unescaped. Duplicate
    parameters: last wins. Raises ValueError on a malformed media type or a
    parameter field without '='.
    """
    if not isinstance(value, str):
        raise ValueError("value must be a string")
    fields = _split_fields(value)
    media = fields[0].strip().lower()
    if media.count("/") != 1:
        raise ValueError(f"invalid media type: {media!r}")
    type_, subtype = media.split("/")
    if type_ == "" or subtype == "":
        raise ValueError(f"invalid media type: {media!r}")
    params: dict[str, str] = {}
    for field in fields[1:]:
        stripped = field.strip()
        if stripped == "":
            continue
        if "=" not in stripped:
            raise ValueError(f"parameter without '=': {field!r}")
        raw_name, raw_value = stripped.split("=", 1)
        name = raw_name.strip().lower()
        pvalue = raw_value.strip()
        if pvalue.startswith('"'):
            pvalue = _unquote(pvalue)
        params[name] = pvalue
    return media, params
