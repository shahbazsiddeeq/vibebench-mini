def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters (excluding the line terminator)
    is strictly greater than limit.

    Lines are obtained with Python's str.splitlines(), so every boundary it recognizes
    splits a line - "\n", "\r", and "\r\n" (each a single terminator), plus form feed "\f",
    vertical tab "\v", and the other Unicode line boundaries; a tab "\t" is NOT a line
    boundary and counts as one character of length.

    Raises ValueError if limit < 1.

    Example: a 3-line source where line 2 has 100 chars -> [2].
    Example: "abc\x0c" followed by 80 x's splits into two lines and returns [2].
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")

    lines = source.splitlines()
    long_line_numbers = []

    for i, line in enumerate(lines):
        if len(line) > limit:
            long_line_numbers.append(i + 1)  # 1-based line numbers

    return long_line_numbers
