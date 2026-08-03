def reverse_words(s):
    """
    Returns a string with the whitespace-separated words of s in reverse order,
    joined by a single space. Words are maximal runs of non-whitespace characters;
    any run of whitespace acts as a separator and is collapsed, and leading/trailing
    whitespace is ignored.
    
    Args:
        s: A string that may contain words separated by whitespace
        
    Returns:
        A string with words in reverse order, joined by single spaces.
        Returns "" if the string is empty or contains only whitespace.
    """
    # Split by whitespace (handles multiple spaces, tabs, newlines, etc.)
    # split() without arguments splits on any whitespace and removes empty strings
    words = s.split()
    
    # Reverse the list of words and join with single space
    return " ".join(reversed(words))
