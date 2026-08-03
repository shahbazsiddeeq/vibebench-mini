def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome after filtering.
    
    Keeps only ASCII alphanumeric characters [A-Za-z0-9], lowercases them,
    and ignores all other characters (spaces, punctuation, non-ASCII).
    Empty strings and strings that reduce to empty return True.
    
    Args:
        s: The string to check
        
    Returns:
        True if the filtered string is a palindrome, False otherwise
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Filter to keep only ASCII alphanumeric characters and lowercase
    filtered = ''.join(c.lower() for c in s if c.isascii() and c.isalnum())
    
    # Check if filtered string is a palindrome
    return filtered == filtered[::-1]
