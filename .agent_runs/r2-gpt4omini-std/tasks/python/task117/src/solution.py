# src/solution.py

def int_to_base(n, base):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if base < 2 or base > 36:
        raise ValueError("base must be in the range [2, 36]")

    if n == 0:
        return "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []

    while n > 0:
        result.append(digits[n % base])
        n //= base

    return ''.join(reversed(result))
