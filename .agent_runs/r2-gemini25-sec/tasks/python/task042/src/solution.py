def word_wrap(text: str, width: int) -> list[str]:
    """
    Wraps text to width characters without breaking words.

    Args:
        text: The input string to wrap.
        width: The maximum width of each line.

    Returns:
        A list of strings, where each string is a wrapped line.

    Raises:
        ValueError: If any single word exceeds the specified width,
                    or if width is non-positive, or if text is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input 'text' must be a string.")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("Input 'width' must be a positive integer.")

    words = text.split()
    if not words:
        return []

    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds specified width {width}.")

    lines = []
    current_line_words = []
    current_line_length = 0

    for word in words:
        # Calculate length if word were added to current line
        # +1 for the space if it's not the first word in the line
        potential_length = current_line_length + (len(word) if not current_line_words else len(word) + 1)

        if potential_length <= width:
            current_line_words.append(word)
            current_line_length = potential_length
        else:
            # Current word doesn't fit, start a new line
            if current_line_words:  # Only add if there are words to form a line
                lines.append(" ".join(current_line_words))
            current_line_words = [word]
            current_line_length = len(word)

    # Add the last line if it's not empty
    if current_line_words:
        lines.append(" ".join(current_line_words))

    return lines
