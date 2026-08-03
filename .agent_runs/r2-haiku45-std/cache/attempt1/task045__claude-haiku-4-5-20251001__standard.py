def validate_isbn13(isbn):
    """
    Validate an ISBN-13 checksum.
    
    Strips hyphens and spaces first, then validates:
    - Length must be exactly 13 digits
    - All characters (after stripping) must be digits
    - Checksum must be valid
    
    Args:
        isbn: A string representing an ISBN-13
        
    Returns:
        True if the ISBN-13 is valid
        
    Raises:
        ValueError: If the ISBN contains non-digit characters (after stripping)
                   or has incorrect length
    """
    # Strip hyphens and spaces
    cleaned_isbn = isbn.replace("-", "").replace(" ", "")
    
    # Check length
    if len(cleaned_isbn) != 13:
        raise ValueError(f"ISBN-13 must be exactly 13 digits, got {len(cleaned_isbn)}")
    
    # Check that all characters are digits
    if not cleaned_isbn.isdigit():
        raise ValueError("ISBN-13 must contain only digits (after stripping hyphens/spaces)")
    
    # Validate checksum
    # ISBN-13 checksum algorithm:
    # 1. Sum digits at odd positions (1st, 3rd, 5th, etc.) with weight 1
    # 2. Sum digits at even positions (2nd, 4th, 6th, etc.) with weight 3
    # 3. Total sum modulo 10 should equal 0
    
    total = 0
    for i, digit in enumerate(cleaned_isbn):
        weight = 1 if i % 2 == 0 else 3
        total += int(digit) * weight
    
    return total % 10 == 0
