def int_to_base(n, base):
    """
    Convert a non-negative integer to a string in the given base (2-36).
    
    Args:
        n: Non-negative integer to convert
        base: Target base (must be between 2 and 36 inclusive)
        
    Returns:
        String representation of n in the given base, using digits 0-9 and letters a-z
        
    Raises:
        ValueError: If n is negative or base is not in range [2, 36]
    """
    # Validate inputs
    if not isinstance(n, int) or not isinstance(base, int):
        raise ValueError("Both n and base must be integers")
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36 inclusive")
    
    # Special case for zero
    if n == 0:
        return "0"
    
    # Characters to use for digits (0-9, a-z)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    result = []
    while n > 0:
        remainder = n % base
        result.append(digits[remainder])
        n //= base
    
    # Reverse since we built it backwards
    return ''.join(reversed(result))
