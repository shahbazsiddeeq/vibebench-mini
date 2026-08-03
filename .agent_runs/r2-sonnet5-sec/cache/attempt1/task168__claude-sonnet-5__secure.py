"""
src/solution.py

Parse an HTTP Content-Type (media-type) header value into a
(media_type, params) tuple, honoring RFC 2616 quoted-string semantics
so that ';' characters inside double-quoted parameter values do not
split fields.

This module is standard-library only and performs strict input
validation. It never uses eval/exec and does not leak internal
exception details beyond a plain ValueError with a safe message.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def _split_fields(value: str) -> List[str]:
    """
    Split `value` on ';' characters, but do not split on ';' that
    occur inside a double-quoted string. Backslash escapes inside a
    quoted string are honored so that an escaped quote (\\") does not
    terminate the quoted string.
    """
    fields: List[str] = []
    current: List[str] = []
    in_quotes = False
    i = 0
    n = len(value)

    while i < n:
        ch = value[i]

        if in_quotes:
            if ch == "\\" and i + 1 < n:
                # Preserve the escape sequence as-is; unescaping is
                # done later when the field is identified as a param
                # value.
                current.append(ch)
                current.append(value[i + 1])
                i += 2
                continue
            elif ch == '"':
                in_quotes = False
                current.append(ch)
                i += 1
                continue
            else:
                current.append(ch)
                i += 1
                continue
        else:
            if ch == '"':
                in_quotes = True
                current.append(ch)
                i += 1
                continue
            elif ch == ";":
                fields.append("".join(current))
                current = []
                i += 1
                continue
            else:
                current.append(ch)
                i += 1
                continue

    fields.append("".join(current))
    return fields


def _unescape_quoted_string(raw: str) -> str:
    """
    Given a string that starts with a double quote, extract the
    RFC 2616 quoted-string contents: strip the surrounding quotes and
    unescape backslash sequences ('\\x' -> 'x').

    If there is no matching closing quote, the remainder (after the
    opening quote) is treated as the content, with escapes still
    processed.
    """
    assert raw.startswith('"')
    body = raw[1:]

    # Find the closing, unescaped quote.
    result_chars: List[str] = []
    i = 0
    n = len(body)
    closed = False

    while i < n:
        ch = body[i]
        if ch == "\\" and i + 1 < n:
            result_chars.append(body[i + 1])
            i += 2
            continue
        elif ch == '"':
            closed = True
            i += 1
            break
        else:
            result_chars.append(ch)
            i += 1
            continue

    # Anything after the closing quote is ignored (not expected in
    # well-formed headers); if never closed, we just use what we have.
    return "".join(result_chars)


def _parse_param(field: str) -> Tuple[str, str]:
    """
    Parse a single 'name=value' parameter field. Raises ValueError if
    there is no '=' present.
    """
    if "=" not in field:
        raise ValueError("Invalid Content-Type parameter: missing '='")

    name, _, raw_value = field.partition("=")
    name = name.strip().lower()
    raw_value = raw_value.strip()

    if not name:
        raise ValueError("Invalid Content-Type parameter: empty name")

    if raw_value.startswith('"'):
        value = _unescape_quoted_string(raw_value)
    else:
        value = raw_value

    return name, value


def parse_content_type(value: str) -> Tuple[str, Dict[str, str]]:
    """
    Parse an HTTP Content-Type header value into (media_type, params).

    Raises:
        ValueError: if the input is not a string, or if the media
            type portion is malformed, or if a parameter field lacks
            an '=' sign.
    """
    if not isinstance(value, str):
        raise ValueError("Content-Type value must be a string")

    fields = _split_fields(value)

    if not fields:
        raise ValueError("Content-Type value is empty")

    media_type_field = fields[0].strip().lower()

    if media_type_field.count("/") != 1:
        raise ValueError("Invalid media type: must contain exactly one '/'")

    type_part, subtype_part = media_type_field.split("/", 1)

    if not type_part or not subtype_part:
        raise ValueError("Invalid media type: type and subtype must be non-empty")

    media_type = f"{type_part}/{subtype_part}"

    params: Dict[str, str] = {}

    for raw_field in fields[1:]:
        field = raw_field.strip()
        if not field:
            # Skip empty fields caused by doubled or trailing ';'
            continue
        name, val = _parse_param(field)
        # Duplicate names: last occurrence wins (dict assignment does this).
        params[name] = val

    return media_type, params
