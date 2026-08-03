def long_lines(source: str, limit: int = 79) -> list[int]:
    """Return 1-based numbers of lines longer than *limit* characters."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    return [
        line_number
        for line_number, line in enumerate(source.splitlines(), start=1)
        if len(line) > limit
    ]
