"""Utilities for parsing RFC 5322-style email headers."""

from __future__ import annotations

__all__ = ["parse_email_headers"]


def _normalize_header_name(name: str) -> str:
    """Return a header name normalized to Title-Case."""
    return "-".join(part[:1].upper() + part[1:].lower() for part in name.split("-"))


def _is_valid_header_name(name: str) -> bool:
    """Validate an RFC 5322 field name."""
    return bool(name) and all(33 <= ord(char) <= 126 and char != ":" for char in name)


def parse_email_headers(raw: str) -> dict[str, str]:
    """Parse RFC 5322-style headers from *raw*.

    Continuation lines are unfolded using one space, duplicate fields are
    replaced by their last occurrence, and parsing stops at the first blank
    line.
    """
    if not isinstance(raw, str):
        raise TypeError("raw must be a string")

    headers: dict[str, str] = {}
    current_name: str | None = None

    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")

    for line in normalized.split("\n"):
        if line == "":
            break

        if line.startswith((" ", "\t")):
            if current_name is not None:
                continuation = line.strip()
                existing = headers[current_name]
                if existing and continuation:
                    headers[current_name] = f"{existing} {continuation}"
                elif continuation:
                    headers[current_name] = continuation
            continue

        current_name = None

        if ":" not in line:
            continue

        name, value = line.split(":", 1)
        if not _is_valid_header_name(name):
            continue

        normalized_name = _normalize_header_name(name)
        headers[normalized_name] = value.strip()
        current_name = normalized_name

    return headers
