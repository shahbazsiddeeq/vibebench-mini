def word_wrap(text, width):
    """
    Wraps text to width characters without breaking words.
    
    Args:
        text: The text to wrap
        width: The maximum width of each line
        
    Returns:
        A list of lines, each with length <= width
        
    Raises:
        ValueError: If any single word exceeds width
    """
    words = text.split()
    
    # Check if any word exceeds width
    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds width {width}")
    
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        # Calculate length if we add this word
        if current_line:
            # Need to account for space before the word
            needed_length = current_length + 1 + word_length
        else:
            # First word on the line
            needed_length = word_length
        
        if needed_length <= width:
            # Word fits on current line
            current_line.append(word)
            current_length = needed_length
        else:
            # Word doesn't fit, start a new line
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length
    
    # Add the last line if it's not empty
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines
