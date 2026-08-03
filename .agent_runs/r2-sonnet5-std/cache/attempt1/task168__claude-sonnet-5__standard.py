"""
Parse Content-Type Header

Provides parse_content_type(value) -> (media_type, params) following
the rules described in the task: ';' separated fields (but not inside
quoted strings), first field is the media type (lower-cased,
'type/subtype'), remaining fields are name=value parameters (name
lower-cased, value quoted-string-unescaped if quoted, else verbatim).
"""

from __future__ import annotations


def _split_fields(value: str) -> list[str]:
    """Split `value` on ';' but not when inside a double-quoted string."""
    fields: list[str] = []
    cur: list[str] = []
    in_quotes = False
    escape = False

    for ch in value:
        if escape:
            cur.append(ch)
            escape = False
            continue

        if ch == "\\" and in_quotes:
            cur.append(ch)
            escape = True
            continue

        if ch == '"':
            in_quotes = not in_quotes
            cur.append(ch)
            continue

        if ch == ";" and not in_quotes:
            fields.append("".join(cur))
            cur = []
            continue

        cur.append(ch)

    fields.append("".join(cur))
    return fields


def _unquote(raw: str) -> str:
    """Remove surrounding quotes from a quoted-string and unescape backslashes."""
    if raw.startswith('"') and raw.endswith('"') and len(raw) >= 2:
        inner = raw[1:-1]
    else:
        # Malformed (starts with quote but no matching closing quote);
        # just strip the leading quote.
        inner = raw[1:]

    result: list[str] = []
    i = 0
    n = len(inner)
    while i < n:
        c = inner[i]
        if c == "\\" and i + 1 < n:
            result.append(inner[i + 1])
            i += 2
        else:
            result.append(c)
            i += 1
    return "".join(result)


def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    fields = _split_fields(value)

    if not fields:
        raise ValueError("Empty Content-Type header value")

    media_type_field = fields[0].strip().lower()
    parts = media_type_field.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError(f"Invalid media type: {fields[0]!r}")

    media_type = media_type_field
    params: dict[str, str] = {}

    for field in fields[1:]:
        stripped = field.strip()
        if not stripped:
            continue

        if "=" not in stripped:
            raise ValueError(f"Invalid parameter field: {field!r}")

        name, _, raw_val = stripped.partition("=")
        name = name.strip().lower()
        raw_val = raw_val.strip()

        if raw_val.startswith('"'):
            val = _unquote(raw_val)
        else:
            val = raw_val

        params[name] = val

    return media_type, params
