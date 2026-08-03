def reverse_words(s):
    """
    Returns a string with the whitespace-separated words of s in reverse order,
    joined by a single space.
    
    Words are maximal runs of non-whitespace characters.
    Any run of whitespace acts as a separator and is collapsed.
    Leading/trailing whitespace is ignored.
    Returns "" for empty or whitespace-only strings.
    """
    words = s.split()
    return ' '.join(reversed(words))
