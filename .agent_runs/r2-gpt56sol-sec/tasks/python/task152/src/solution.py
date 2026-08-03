"""Utilities for parsing dotenv files."""

from __future__ import annotations

import re

_KEY_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_DOUBLE_QUOTE_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    '"': '"',
}


def _unescape_double_quoted(value: str) -> str:
    result: list[str] = []
    index = 0

    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            escaped = value[index + 1]
            replacement = _DOUBLE_QUOTE_ESCAPES.get(escaped)
            if replacement is not None:
                result.append(replacement)
                index += 2
                continue

        result.append(char)
        index += 1

    return "".join(result)


def _parse_value(raw_value: str) -> str:
    if (
        len(raw_value) >= 2
        and raw_value.startswith('"')
        and raw_value.endswith('"')
    ):
        return _unescape_double_quoted(raw_value[1:-1])

    if (
        len(raw_value) >= 2
        and raw_value.startswith("'")
        and raw_value.endswith("'")
    ):
        return raw_value[1:-1]

    comment_index = None
    for index, char in enumerate(raw_value):
        if char == "#" and (index == 0 or raw_value[index - 1].isspace()):
            comment_index = index
            break

    if comment_index is not None:
        raw_value = raw_value[:comment_index]

    return raw_value.strip()


def parse_dotenv(path: str) -> dict[str, str]:
    """Parse a UTF-8 dotenv file and return its key-value pairs."""
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if "\x00" in path:
        raise ValueError("path contains an invalid character")

    result: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as dotenv_file:
        for source_line in dotenv_file:
            line = source_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line[len("export "):]

            if "=" not in line:
                raise ValueError("invalid dotenv assignment")

            key_text, raw_value = line.split("=", 1)
            key = key_text.strip()

            if not key or _KEY_PATTERN.fullmatch(key) is None:
                raise ValueError("invalid dotenv key")

            result[key] = _parse_value(raw_value)

    return result
