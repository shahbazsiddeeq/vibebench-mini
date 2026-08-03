def word_wrap(text, width):
    """
    Wraps text to specified width without breaking words.
    
    Args:
        text: String to wrap
        width: Maximum width for each line
        
    Returns:
        List of wrapped lines
        
    Raises:
        ValueError: If any single word exceeds width
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width <= 0:
        raise ValueError("width must be positive")
    
    # Handle empty string
    if not text:
        return []
    
    # Split text into words
    words = text.split()
    
    # Handle empty after split (only whitespace)
    if not words:
        return []
    
    # Check if any word exceeds width
    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds width {width}")
    
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        # If this is the first word in the line
        if not current_line:
            current_line.append(word)
            current_length = word_length
        else:
            # Check if adding this word (with a space) would exceed width
            # current_length + 1 (space) + word_length
            if current_length + 1 + word_length <= width:
                current_line.append(word)
                current_length += 1 + word_length
            else:
                # Start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
    
    # Add the last line if there is one
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
