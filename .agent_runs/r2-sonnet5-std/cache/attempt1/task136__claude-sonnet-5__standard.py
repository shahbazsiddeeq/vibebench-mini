def long_lines(source, limit=79):
    if limit < 1:
        raise ValueError("limit must be >= 1")
    lines = source.splitlines()
    return [i for i, line in enumerate(lines, start=1) if len(line) > limit]
