# src/solution.py

def int_to_base(n, base):
    if not isinstance(n, int) or not isinstance(base, int):
        raise TypeError("Both n and base must be integers.")
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36, inclusive.")
    
    if n == 0:
        return "0"
    
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []
    
    while n > 0:
        n, remainder = divmod(n, base)
        result.append(digits[remainder])
    
    return ''.join(reversed(result))
