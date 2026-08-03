def int_to_base(n, base):
    """
    Convert a non-negative integer to a string in the given base (2-36).
    Uses digits 0-9 then a-z.
    
    Args:
        n: Non-negative integer to convert
        base: Base to convert to (2-36)
    
    Returns:
        String representation of n in the given base
    
    Raises:
        ValueError: If n < 0 or base not in [2, 36]
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36")
    
    if n == 0:
        return "0"
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    
    while n > 0:
        result = digits[n % base] + result
        n //= base
    
    return result
