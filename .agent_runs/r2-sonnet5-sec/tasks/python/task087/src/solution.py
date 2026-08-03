"""
src/solution.py

A small, security-conscious Cookie header parser.

The public function `parse_cookie` parses a Cookie header string of the
form "key=value; key2=value2" into a dict, following these rules:

  - Cookie pairs are split on ';'.
  - Each pair is split on the FIRST '=' only, so values may themselves
    contain '=' characters (e.g. base64 padding) without being truncated.
  - Surrounding whitespace around keys and values is trimmed.
  - Segments with no '=' are ignored (they are not valid key=value pairs).
  - For duplicate keys, the last occurrence wins.

This module only relies on the Python standard library and performs no
I/O. All external input is treated as untrusted and validated before use.
"""

from __future__ import annotations

from typing import Dict


def parse_cookie(header: object) -> Dict[str, str]:
    """Parse a Cookie header string into a dictionary of key/value pairs.

    Args:
        header: The raw Cookie header value. Expected to be a ``str``.

    Returns:
        A dict mapping cookie names to their (unescaped, trimmed) values.
        If ``header`` is empty, ``None`` or not a string, an empty dict
        is returned rather than raising, to avoid leaking internal error
        details to callers processing untrusted input.
    """
    # Defensive validation: never trust external input's type or shape.
    if header is None:
        return {}
    if not isinstance(header, str):
        return {}

    result: Dict[str, str] = {}

    # Guard against pathologically huge headers to avoid excessive
    # memory/CPU usage on untrusted input.
    max_header_length = 1 << 20  # 1 MiB is far more than any real cookie header
    if len(header) > max_header_length:
        header = header[:max_header_length]

    for segment in header.split(";"):
        if "=" not in segment:
            # No '=' present -> not a valid key=value pair; ignore it.
            continue

        key, value = segment.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            # Ignore entries with an empty key after trimming.
            continue

        # Last occurrence wins for duplicate keys.
        result[key] = value

    return result
