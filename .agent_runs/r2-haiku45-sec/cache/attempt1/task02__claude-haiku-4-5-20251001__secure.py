def reverse_words(s):
    """
    Reverse the order of whitespace-separated words in a string.
    
    Words are maximal runs of non-whitespace characters. Any run of whitespace
    (spaces, tabs, newlines) acts as a separator and is collapsed. Leading and
    trailing whitespace is ignored.
    
    Args:
        s: A string to process
        
    Returns:
        A string with words in reverse order, joined by single spaces.
        Returns empty string if input is empty or contains only whitespace.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Split on any whitespace and filter out empty strings
    # split() without arguments splits on any whitespace and removes empty strings
    words = s.split()
    
    # Reverse the list of words and join with single space
    return " ".join(reversed(words))
