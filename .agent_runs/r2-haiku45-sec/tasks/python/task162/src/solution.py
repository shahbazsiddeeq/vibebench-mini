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
        raise ValueError("number must contain only ASCII digits 0-9")
    
    total = 0
    # Process digits from right to left
    for position, digit in enumerate(reversed(number), start=1):
        digit_value = int(digit)
        
        # Double every second digit (positions 2, 4, 6, ... from the right)
        if position % 2 == 0:
            digit_value *= 2
            # Subtract 9 if the doubled value is greater than 9
            if digit_value > 9:
                digit_value -= 9
        
        total += digit_value
    
    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    """
    Calculate the check digit that makes a payload Luhn-valid.
    
    Args:
        payload: A string of digits (without the check digit)
        
    Returns:
        The check digit (0-9) that when appended makes the full string valid
        
    Raises:
        TypeError: If payload is not a string
        ValueError: If payload is empty or contains non-digit characters
    """
    if not isinstance(payload, str):
        raise TypeError("payload must be a string")
    
    if len(payload) == 0:
        raise ValueError("payload cannot be empty")
    
    if not all(c in '0123456789' for c in payload):
        raise ValueError("payload must contain only ASCII digits 0-9")
    
    # Try each possible check digit (0-9) and find which one makes it valid
    for check_digit in range(10):
        full_number = payload + str(check_digit)
        if luhn_valid(full_number):
            return check_digit
    
    # This should never happen if the algorithm is correct
    return 0
