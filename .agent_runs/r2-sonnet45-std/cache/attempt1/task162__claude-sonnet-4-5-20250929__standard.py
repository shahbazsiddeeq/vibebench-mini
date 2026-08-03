def luhn_valid(number: str) -> bool:
    """
    Validate a number string using the Luhn mod-10 algorithm.
    
    Args:
        number: A string of digits including the check digit
        
    Returns:
        True if the number passes Luhn validation, False otherwise
        
    Raises:
        TypeError: If number is not a string
        ValueError: If number is empty or contains non-digit characters
    """
    # Validate input type
    if not isinstance(number, str):
        raise TypeError("Argument must be a string")
    
    # Validate non-empty
    if not number:
        raise ValueError("String cannot be empty")
    
    # Validate all characters are digits
    if not all(c in '0123456789' for c in number):
        raise ValueError("String must contain only digits 0-9")
    
    # Process digits from right to left
    total = 0
    for i, digit in enumerate(reversed(number)):
        d = int(digit)
        # Position 1 is rightmost (i=0), position 2 is i=1, etc.
        # Double every second digit (positions 2, 4, 6... which are i=1, 3, 5...)
        if i % 2 == 1:  # positions 2, 4, 6... (0-indexed: 1, 3, 5...)
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    """
    Calculate the Luhn check digit for a payload string.
    
    Args:
        payload: A string of digits (without check digit)
        
    Returns:
        The check digit (0-9) that makes payload + check_digit valid
        
    Raises:
        TypeError: If payload is not a string
        ValueError: If payload is empty or contains non-digit characters
    """
    # Validate input type
    if not isinstance(payload, str):
        raise TypeError("Argument must be a string")
    
    # Validate non-empty
    if not payload:
        raise ValueError("String cannot be empty")
    
    # Validate all characters are digits
    if not all(c in '0123456789' for c in payload):
        raise ValueError("String must contain only digits 0-9")
    
    # Calculate sum for the payload
    # When we append a check digit, it will be at position 1 (rightmost)
    # So current rightmost digit of payload will be at position 2
    total = 0
    for i, digit in enumerate(reversed(payload)):
        d = int(digit)
        # After appending check digit, these positions shift by 1
        # Current i=0 becomes position 2, i=1 becomes position 3, etc.
        # So we double at i=0, 2, 4... (which will be positions 2, 4, 6...)
        if i % 2 == 0:  # positions 2, 4, 6... after check digit is added
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    # Find check digit that makes (total + check_digit) % 10 == 0
    check_digit = (10 - (total % 10)) % 10
    return check_digit
