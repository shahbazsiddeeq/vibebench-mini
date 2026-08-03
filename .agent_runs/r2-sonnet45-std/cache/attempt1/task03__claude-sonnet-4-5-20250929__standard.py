def is_palindrome(s):
    """
    Returns True if s reads the same forwards and backwards after keeping only
    ASCII alphanumeric characters and lowercasing them.
    
    Args:
        s: Input string
        
    Returns:
        bool: True if the filtered string is a palindrome, False otherwise
    """
    # Filter to keep only ASCII alphanumeric characters and lowercase
    filtered = ''.join(c.lower() for c in s if c.isascii() and c.isalnum())
    
    # Check if palindrome
    return filtered == filtered[::-1]
