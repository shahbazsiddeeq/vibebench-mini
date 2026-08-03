"""Utilities for detecting lines that exceed a character limit."""


def long_lines(source: str, limit: int = 79) -> list[int]:
    """Return 1-based numbers of lines whose lengths are greater than limit."""
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be at least 1")

    return [
        line_number
        for line_number, line in enumerate(source.splitlines(), start=1)
        if len(line) > limit
    ]
