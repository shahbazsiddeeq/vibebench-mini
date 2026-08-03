"""Utilities for parsing HTTP Content-Type header values."""

from __future__ import annotations


def _split_fields(value: str) -> list[str]:
    """Split on semicolons that are outside quoted strings."""
    fields: list[str] = []
    current: list[str] = []
    in_quotes = False
    escaped = False

    for character in value:
        if in_quotes:
            current.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_quotes = False
        else:
            if character == '"':
                in_quotes = True
                current.append(character)
            elif character == ";":
                fields.append("".join(current))
                current = []
            else:
                current.append(character)

    if in_quotes:
        raise ValueError("unterminated quoted string")

    fields.append("".join(current))
    return fields


def _parse_quoted_value(value: str) -> str:
    """Remove surrounding quotes and decode quoted-pair escapes."""
    if len(value) < 2 or value[-1] != '"':
        raise ValueError("invalid quoted parameter value")

    result: list[str] = []
    escaped = False

    for character in value[1:-1]:
        if escaped:
            result.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == '"':
            raise ValueError("invalid quote in parameter value")
        else:
            result.append(character)

    if escaped:
        raise ValueError("incomplete escape in parameter value")

    return "".join(result)


def parse_content_type(value: str) -> tuple[str, dict[str, str]]:
    """Parse an HTTP Content-Type or media-type header value."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    fields = _split_fields(value)
    media_type = fields[0].strip()

    if media_type.count("/") != 1:
        raise ValueError("invalid media type")

    type_name, subtype_name = media_type.split("/", 1)
    if not type_name or not subtype_name:
        raise ValueError("invalid media type")

    media_type = media_type.lower()
    parameters: dict[str, str] = {}

    for field in fields[1:]:
        field = field.strip()
        if not field:
            continue

        if "=" not in field:
            raise ValueError("invalid parameter")

        name, parameter_value = field.split("=", 1)
        name = name.strip().lower()
        parameter_value = parameter_value.strip()

        if not name:
            raise ValueError("parameter name cannot be empty")

        if parameter_value.startswith('"'):
            parameter_value = _parse_quoted_value(parameter_value)

        parameters[name] = parameter_value

    return media_type, parameters
