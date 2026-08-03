"""Utilities for parsing HTTP Content-Type header values."""


def _split_fields(value: str) -> list[str]:
    """Split on semicolons that are outside double-quoted strings."""
    fields: list[str] = []
    start = 0
    in_quotes = False
    escaped = False

    for index, char in enumerate(value):
        if in_quotes:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quotes = False
        elif char == '"':
            in_quotes = True
        elif char == ";":
            fields.append(value[start:index])
            start = index + 1

    if in_quotes or escaped:
        raise ValueError("unterminated quoted string")

    fields.append(value[start:])
    return fields


def _parse_quoted_string(value: str) -> str:
    """Remove surrounding quotes and unescape RFC-2616 quoted pairs."""
    if len(value) < 2 or value[-1] != '"':
        raise ValueError("unterminated quoted parameter value")

    result: list[str] = []
    escaped = False

    for char in value[1:-1]:
        if escaped:
            result.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            raise ValueError("unexpected quote in parameter value")
        else:
            result.append(char)

    if escaped:
        raise ValueError("incomplete quoted-pair")

    return "".join(result)


def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """Parse an HTTP Content-Type or media-type header value."""
    fields = _split_fields(value)

    media_type = fields[0].strip().lower()
    if media_type.count("/") != 1:
        raise ValueError("media type must contain exactly one '/'")

    type_name, subtype = media_type.split("/", 1)
    if not type_name or not subtype:
        raise ValueError("media type and subtype must be non-empty")

    params: dict[str, str] = {}

    for field in fields[1:]:
        field = field.strip()
        if not field:
            continue

        if "=" not in field:
            raise ValueError("parameter field must contain '='")

        name, parameter_value = field.split("=", 1)
        name = name.strip().lower()
        if not name:
            raise ValueError("parameter name must be non-empty")

        parameter_value = parameter_value.strip()
        if parameter_value.startswith('"'):
            parameter_value = _parse_quoted_string(parameter_value)

        params[name] = parameter_value

    return media_type, params
