def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome after filtering and normalizing.
    
    Only ASCII alphanumeric characters ([A-Za-z0-9]) are kept.
    All other characters (spaces, punctuation, non-ASCII) are ignored.
    Comparison is case-insensitive.
    Empty string or string that reduces to empty returns True.
    
    Args:
        s: Input string to check
        
    Returns:
        True if the filtered string is a palindrome, False otherwise
    """
    # Input validation
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Filter to keep only ASCII alphanumeric characters and convert to lowercase
    filtered = []
    for char in s:
        # Check if character is ASCII alphanumeric
        if char.isalnum() and ord(char) < 128:
            filtered.append(char.lower())
    
    # Convert to string for comparison
    filtered_str = ''.join(filtered)
    
    # Check if palindrome by comparing with reverse
    return filtered_str == filtered_str[::-1]
