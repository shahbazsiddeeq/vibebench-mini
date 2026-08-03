def int_to_base(n: int, base: int) -> str:
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 2 <= base <= 36:
        raise ValueError("base must be in [2, 36]")
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []
    while n:
        result.append(digits[n % base])
        n //= base
    return "".join(reversed(result))
