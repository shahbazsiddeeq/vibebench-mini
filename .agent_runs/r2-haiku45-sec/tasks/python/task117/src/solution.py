def int_to_base(n, base):
    """
    Convert a non-negative integer to a string in the given base (2-36).
    
    Uses digits 0-9 then a-z for bases up to 36.
    
    Args:
        n: Non-negative integer to convert
        base: Base to convert to (must be between 2 and 36 inclusive)
    
    Returns:
        String representation of n in the given base
    
    Raises:
        ValueError: If n is negative or base is not in [2, 36]
    """
    # Validate inputs
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer")
    
    if not isinstance(base, int) or isinstance(base, bool):
        raise ValueError("base must be an integer")
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36 inclusive")
    
    # Special case for zero
    if n == 0:
        return "0"
    
    # Digit characters: 0-9, then a-z
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    result = []
    while n > 0:
        result.append(digits[n % base])
        n //= base
    
    # Reverse to get correct order
    return "".join(reversed(result))
