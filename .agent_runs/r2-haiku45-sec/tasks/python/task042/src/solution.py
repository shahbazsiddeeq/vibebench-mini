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
    # Input validation
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    
    # Handle empty string
    if not text:
        return []
    
    # Split text into words
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
        # If current_line is empty, length is just word_length
        # Otherwise, we need to account for the space before the word
        if current_line:
            potential_length = current_length + 1 + word_length  # +1 for space
        else:
            potential_length = word_length
        
        # If adding this word would exceed width, start a new line
        if current_line and potential_length > width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length = potential_length
    
    # Add the last line if it's not empty
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines
