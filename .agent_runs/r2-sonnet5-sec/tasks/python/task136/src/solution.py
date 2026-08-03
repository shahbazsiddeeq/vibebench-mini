"""Long Line Linter.

Provides a function to detect lines in a source text exceeding a
specified length limit.
"""

from typing import List


def long_lines(source: str, limit: int = 79) -> List[int]:
    """Return 1-based line numbers whose length exceeds `limit` characters.

    Lines are split using str.splitlines(), which recognizes all Unicode
    line boundaries (e.g. "\\n", "\\r", "\\r\\n", "\\f", "\\v", etc.).
    A tab character does not count as a line boundary.

    Args:
        source: The text to analyze.
        limit: Maximum allowed line length (must be >= 1).

    Returns:
        A list of 1-based line numbers whose length is strictly greater
        than `limit`.

    Raises:
        ValueError: If `limit` is less than 1.
        TypeError: If `source` is not a string or `limit` is not an int.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an int")
    if limit < 1:
        raise ValueError("limit must be >= 1")

    lines = source.splitlines()
    return [
        idx
        for idx, line in enumerate(lines, start=1)
        if len(line) > limit
    ]
