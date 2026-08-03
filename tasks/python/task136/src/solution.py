from __future__ import annotations


def long_lines(source: str, limit: int = 79) -> list[int]:
    """Return 1-based line numbers longer than ``limit`` characters.

    Line length excludes the trailing newline. Raises ValueError if limit < 1.
    """
    if limit < 1:
        raise ValueError("limit must be >= 1")

    result: list[int] = []
    for index, line in enumerate(source.splitlines(), start=1):
        if len(line) > limit:
            result.append(index)
    return result
