def luhn_valid(number: str) -> bool:
    """
    Validate a number using the Luhn mod-10 algorithm.
    
    Args:
        number: A string of digits that includes the check digit
        
    Returns:
        True if the number satisfies the Luhn checksum, False otherwise
        
    Raises:
        TypeError: If number is not a string
        ValueError: If number is empty or contains non-digit characters
    """
    if not isinstance(number, str):
        raise TypeError("number must be a string")
    
    if len(number) == 0:
        raise ValueError("number cannot be empty")
    
    if not all(c in '0123456789' for c in number):
        raise ValueError("number must contain only digits")
    
    # Process digits from right to left
    total = 0
    for i, digit in enumerate(reversed(number)):
        d = int(digit)
        # Position 1 is rightmost, position 2 is second from right, etc.
        # We double every second digit (positions 2, 4, 6, ...)
        if (i + 1) % 2 == 0:  # Every second position (0-indexed: 1, 3, 5, ...)
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    """
    Calculate the check digit that makes a payload Luhn-valid.
    
    Args:
        payload: A string of digits without the check digit
        
    Returns:
        The check digit (0-9) that when appended makes the string valid
        
    Raises:
        TypeError: If payload is not a string
        ValueError: If payload is empty or contains non-digit characters
    """
    if not isinstance(payload, str):
        raise TypeError("payload must be a string")
    
    if len(payload) == 0:
        raise ValueError("payload cannot be empty")
    
    if not all(c in '0123456789' for c in payload):
        raise ValueError("payload must contain only digits")
    
    # Try each digit 0-9 and find which one makes it valid
    for check_digit in range(10):
        full_number = payload + str(check_digit)
        if luhn_valid(full_number):
            return check_digit
    
    # Should never reach here if algorithm is correct
    return 0
