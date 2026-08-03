def word_wrap(text, width):
    """
    Wraps text to width characters without breaking words.

    Args:
        text (str): The input text to wrap.
        width (int): The maximum width of each line.

    Returns:
        list: A list of strings, where each string is a wrapped line.

    Raises:
        ValueError: If any single word exceeds the specified width.
    """
    if not text:
        return []

    words = text.split()
    if not words:  # Handle cases like "   "
        return []

    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds specified width {width}")

    lines = []
    current_line_words = []
    current_line_length = 0

    for word in words:
        # Calculate length if word is added to current line
        # +1 for the space if it's not the first word in the line
        potential_length = current_line_length + (len(word) + 1 if current_line_words else len(word))

        if potential_length <= width:
            current_line_words.append(word)
            current_line_length = potential_length
        else:
            # Start a new line
            lines.append(" ".join(current_line_words))
            current_line_words = [word]
            current_line_length = len(word)

    # Add the last accumulated line if any
    if current_line_words:
        lines.append(" ".join(current_line_words))

    return lines
