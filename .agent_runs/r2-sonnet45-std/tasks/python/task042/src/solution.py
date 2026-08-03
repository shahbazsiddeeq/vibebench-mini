def word_wrap(text, width):
    """
    Wraps text to width characters without breaking words.
    
    Args:
        text: The text to wrap
        width: Maximum width of each line
        
    Returns:
        List of wrapped lines
        
    Raises:
        ValueError: If any single word exceeds width
    """
    if not text:
        return [""]
    
    words = text.split()
    
    # Check if any word exceeds width
    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds width {width}")
    
    if not words:
        return [""]
    
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        if not current_line:
            # First word on the line
            current_line.append(word)
            current_length = word_length
        else:
            # Check if adding this word (with a space) would exceed width
            potential_length = current_length + 1 + word_length  # +1 for space
            
            if potential_length <= width:
                # Add word to current line
                current_line.append(word)
                current_length = potential_length
            else:
                # Start a new line
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
    
    # Add the last line if there is one
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines
