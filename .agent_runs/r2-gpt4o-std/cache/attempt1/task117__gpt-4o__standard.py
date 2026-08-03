# src/solution.py

def int_to_base(n, base):
    if n < 0:
        raise ValueError("n must be non-negative")
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36")

    if n == 0:
        return "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []

    while n > 0:
        n, remainder = divmod(n, base)
        result.append(digits[remainder])

    return ''.join(reversed(result))
