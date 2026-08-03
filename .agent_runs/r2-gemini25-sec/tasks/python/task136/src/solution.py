def long_lines(source, limit=79):
    """
    Returns the 1-based line numbers whose length in characters (excluding the line terminator)
    is strictly greater than limit.

    Lines are obtained with Python's str.splitlines(), so every boundary it recognizes
    splits a line - "\\n", "\\r", and "\\r\\n" (each a single terminator), plus form feed "\\f",
    vertical tab "\\v", and the other Unicode line boundaries; a tab "\\t" is NOT a line boundary
    and counts as one character of length.

    Args:
        source (str): The input string containing the source code.
        limit (int): The maximum allowed line length. Must be a positive integer.

    Returns:
        list: A list of 1-based line numbers that exceed the limit.

    Raises:
        ValueError: If limit is less than 1.
    """
    if not isinstance(limit, int):
        raise ValueError("limit must be an integer.")
    if limit < 1:
        raise ValueError("limit must be a positive integer.")
    if not isinstance(source, str):
        # Ensure source is a string to prevent unexpected behavior with splitlines
        # and len if a non-string type is passed.
        raise TypeError("source must be a string.")

    lines = source.splitlines()
    long_line_numbers = []

    for i, line in enumerate(lines):
        # The length of the line is simply len(line) because splitlines()
        # already removes the line terminators.
        if len(line) > limit:
            long_line_numbers.append(i + 1)  # 1-based line number

    return long_line_numbers
