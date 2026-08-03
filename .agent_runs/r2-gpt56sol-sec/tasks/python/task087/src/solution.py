"""Utilities for parsing HTTP Cookie header values."""


def parse_cookie(header: str) -> dict[str, str]:
    """Parse a Cookie header into a mapping of cookie names to values."""
    if not isinstance(header, str):
        raise TypeError("header must be a string")

    cookies: dict[str, str] = {}

    for segment in header.split(";"):
        if "=" not in segment:
            continue

        key, value = segment.split("=", 1)
        cookies[key.strip()] = value.strip()

    return cookies
