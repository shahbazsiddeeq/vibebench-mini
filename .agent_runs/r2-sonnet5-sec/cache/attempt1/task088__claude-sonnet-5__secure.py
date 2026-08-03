"""
src/solution.py

A secure, self-contained parser for RFC 5322-style email headers.

Design notes (security-focused):
- Only the Python standard library is used.
- No eval/exec or dynamic code execution.
- All external input is treated as untrusted: type-checked, size-bounded
  parsing logic, and malformed lines are safely skipped rather than
  causing crashes or leaking internal state.
- No randomness is required for this task, but if any were needed we
  would use the `secrets` module rather than `random`.
"""

from __future__ import annotations

import re
from typing import Dict

# Maximum raw input size we are willing to process, to avoid
# unbounded memory/CPU usage from hostile input (defense in depth).
_MAX_INPUT_SIZE = 10 * 1024 * 1024  # 10 MiB

# A valid header field-name per RFC 5322 is one or more printable US-ASCII
# characters excluding the colon (":"), i.e. characters in the range
# 33-126 except 58 (':').
_FIELD_NAME_RE = re.compile(r"^[!-9;-~]+$")


def _normalize_header_name(name: str) -> str:
    """
    Normalize a header field name to Title-Case, splitting on hyphens.

    Example: "content-type" -> "Content-Type"
             "X-Long"       -> "X-Long"
    """
    parts = name.split("-")
    normalized_parts = [part.capitalize() if part else part for part in parts]
    return "-".join(normalized_parts)


def _is_valid_field_name(name: str) -> bool:
    if not name:
        return False
    return bool(_FIELD_NAME_RE.match(name))


def parse_email_headers(raw: str) -> Dict[str, str]:
    """
    Parse RFC 5322-style headers from `raw` into a dictionary.

    Rules implemented:
      - Header names are case-normalized to Title-Case.
      - Folded (continuation) lines -- those starting with a space or tab --
        are joined to the previous header's value with a single space,
        with leading/trailing whitespace stripped from each part.
      - Parsing stops at the first blank line; anything after it (the
        "body") is ignored.
      - Duplicate header names: the last occurrence wins.

    Malformed lines (no colon, empty/invalid field name, or a continuation
    line with no preceding header) are safely skipped rather than raising,
    to avoid leaking parsing internals or crashing on hostile input.

    Args:
        raw: The raw header text (and optionally body) as a string.

    Returns:
        A dict mapping normalized header names to their unfolded values.

    Raises:
        TypeError: if `raw` is not a string.
        ValueError: if `raw` exceeds the maximum allowed size.
    """
    if not isinstance(raw, str):
        raise TypeError("raw must be a string")

    if len(raw) > _MAX_INPUT_SIZE:
        raise ValueError("input too large to process")

    headers: Dict[str, str] = {}

    current_key: str | None = None
    current_parts: list[str] = []

    # Split on '\n' and strip any trailing '\r' to support both LF and
    # CRLF line endings without altering intended content.
    lines = raw.split("\n")

    for line in lines:
        if line.endswith("\r"):
            line = line[:-1]

        # Blank line: end of headers section, stop processing.
        if line == "":
            break

        # Continuation (folded) line: starts with space or tab.
        if line[0] in (" ", "\t"):
            if current_key is None:
                # Continuation with no preceding header; ignore safely.
                continue
            current_parts.append(line.strip())
            continue

        # This is a new header line. Flush the previous header, if any.
        if current_key is not None:
            headers[current_key] = " ".join(current_parts)
            current_key = None
            current_parts = []

        if ":" not in line:
            # Malformed header line; skip it safely.
            continue

        name, _, value = line.partition(":")
        name = name.strip()

        if not _is_valid_field_name(name):
            # Invalid field name; skip this line safely.
            continue

        normalized_name = _normalize_header_name(name)
        current_key = normalized_name
        current_parts = [value.strip()]

    # Flush any pending header at end of input (no trailing blank line).
    if current_key is not None:
        headers[current_key] = " ".join(current_parts)

    return headers
