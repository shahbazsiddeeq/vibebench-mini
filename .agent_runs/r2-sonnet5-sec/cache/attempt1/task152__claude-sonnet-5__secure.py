"""
src/solution.py

A secure, self-contained parser for `.env` style files.

Only the Python standard library is used. The parser is careful to:
  * Validate every input value (keys, escape sequences, etc.).
  * Never use eval/exec or any other dynamic code execution.
  * Fail with clear, non-leaking error messages (no internal state,
    tracebacks, or file contents are echoed back to the caller).
"""

from __future__ import annotations

import re
from typing import Dict

__all__ = ["parse_dotenv"]

# A valid environment variable name: starts with a letter or underscore,
# followed by letters, digits, or underscores.
_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# Mapping of recognised escape sequences inside double-quoted values.
_DOUBLE_QUOTE_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    '"': '"',
}


def _unescape_double_quoted(value: str) -> str:
    """
    Unescape the sequences \\n, \\t, \\r, \\\\ and \\" inside a
    double-quoted value. Any other backslash sequence is left as-is
    (the backslash and following character are kept literally).
    """
    result = []
    i = 0
    length = len(value)
    while i < length:
        ch = value[i]
        if ch == "\\" and i + 1 < length:
            nxt = value[i + 1]
            if nxt in _DOUBLE_QUOTE_ESCAPES:
                result.append(_DOUBLE_QUOTE_ESCAPES[nxt])
                i += 2
                continue
        result.append(ch)
        i += 1
    return "".join(result)


def _strip_inline_comment(raw: str) -> str:
    """
    Strip an inline comment from an *unquoted* value. A comment begins
    at the first '#' that is either at index 0 or immediately preceded
    by whitespace (space or tab).
    """
    for idx, ch in enumerate(raw):
        if ch == "#":
            if idx == 0 or raw[idx - 1] in (" ", "\t"):
                return raw[:idx]
    return raw


def _parse_value(raw: str) -> str:
    """
    Determine the final value from the raw right-hand side of an
    assignment (the text after the first '=', before any stripping).
    """
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        inner = raw[1:-1]
        return _unescape_double_quoted(inner)

    if len(raw) >= 2 and raw[0] == "'" and raw[-1] == "'":
        inner = raw[1:-1]
        return inner

    # Unquoted value: strip inline comment, then surrounding whitespace.
    without_comment = _strip_inline_comment(raw)
    return without_comment.strip()


def parse_dotenv(path: str) -> Dict[str, str]:
    """
    Parse a UTF-8 encoded .env file located at `path` into a dict.

    Rules:
      * Lines are stripped; blank lines and lines beginning with '#'
        (after stripping) are skipped.
      * An optional leading 'export ' prefix is removed.
      * The remainder is split on the FIRST '=' into key and raw value.
        Missing '=' raises ValueError.
      * The key (left of '=', stripped) must match
        ``[A-Za-z_][A-Za-z0-9_]*`` or ValueError is raised.
      * The value is derived from the raw right-hand side per the
        quoting rules described in the module docstring.
      * Later duplicate keys overwrite earlier ones.

    Raises:
        FileNotFoundError: if `path` does not exist.
        ValueError: if a line is malformed or a key is invalid.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    # Let FileNotFoundError propagate naturally; do not swallow it or
    # leak any other exception details beyond what's necessary.
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    result: Dict[str, str] = {}

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue
        if stripped.startswith("#"):
            continue

        if stripped.startswith("export "):
            stripped = stripped[len("export "):]

        if "=" not in stripped:
            raise ValueError("Malformed line: missing '=' separator")

        key_part, raw_value = stripped.split("=", 1)
        key = key_part.strip()

        if not key or not _KEY_RE.match(key):
            raise ValueError(f"Invalid environment variable name: {key!r}")

        value = _parse_value(raw_value)
        result[key] = value

    return result
