def validate_isbn13(isbn):
    """
    Validates an ISBN-13 string.
    
    Args:
        isbn: A string representing an ISBN-13, possibly with hyphens or spaces
        
    Returns:
        True if the ISBN-13 is valid
        
    Raises:
        ValueError: If the input contains non-digit characters (after stripping
                   hyphens/spaces) or has wrong length
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string")
    
    # Strip hyphens and spaces
    cleaned = isbn.replace('-', '').replace(' ', '')
    
    # Validate that only digits remain
    if not cleaned:
        raise ValueError("ISBN cannot be empty")
    
    if not cleaned.isdigit():
        raise ValueError("ISBN must contain only digits (after removing hyphens and spaces)")
    
    # Validate length
    if len(cleaned) != 13:
        raise ValueError("ISBN-13 must be exactly 13 digits")
    
    # Calculate checksum
    total = 0
    for i, digit in enumerate(cleaned):
        digit_value = int(digit)
        # Multiply by 1 for even indices (0, 2, 4...) and by 3 for odd indices (1, 3, 5...)
        multiplier = 1 if i % 2 == 0 else 3
        total += digit_value * multiplier
    
    # Valid if sum is divisible by 10
    return total % 10 == 0
