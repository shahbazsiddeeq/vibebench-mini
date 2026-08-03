def reverse_words(s: str) -> str:
    """
    Reverse the order of whitespace-separated words in a string.
    
    Args:
        s: Input string
        
    Returns:
        String with words in reverse order, joined by single spaces.
        Returns empty string if input is empty or contains only whitespace.
    """
    # Input validation
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # split() with no arguments splits on any whitespace and removes empty strings
    words = s.split()
    
    # Reverse the list of words
    words.reverse()
    
    # Join with single space
    return " ".join(words)
