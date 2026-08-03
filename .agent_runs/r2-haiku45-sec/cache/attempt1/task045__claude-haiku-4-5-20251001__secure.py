def validate_isbn13(isbn: str) -> bool:
    """
    Validate an ISBN-13 checksum.
    
    Strips hyphens and spaces from the input, then validates:
    - Length is exactly 13 digits
    - All characters (after stripping) are digits
    - Checksum is correct
    
    Args:
        isbn: ISBN-13 string, potentially with hyphens or spaces
        
    Returns:
        True if valid ISBN-13 checksum
        
    Raises:
        ValueError: If non-digit characters remain after stripping,
                   or if length is not 13
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string")
    
    # Strip hyphens and spaces
    cleaned = isbn.replace("-", "").replace(" ", "")
    
    # Check length
    if len(cleaned) != 13:
        raise ValueError(f"ISBN-13 must be exactly 13 digits, got {len(cleaned)}")
    
    # Check all characters are digits
    if not cleaned.isdigit():
        raise ValueError("ISBN-13 must contain only digits (after removing hyphens and spaces)")
    
    # Validate checksum
    # ISBN-13 checksum: alternating weights of 1 and 3, starting with 1
    # Sum all weighted digits, checksum digit is (10 - (sum % 10)) % 10
    total = 0
    for i, digit in enumerate(cleaned[:12]):
        weight = 1 if i % 2 == 0 else 3
        total += int(digit) * weight
    
    check_digit = (10 - (total % 10)) % 10
    
    return check_digit == int(cleaned[12])
