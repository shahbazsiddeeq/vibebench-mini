DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def int_to_base(n, base):
    if n < 0:
        raise ValueError("n must be non-negative")
    if base < 2 or base > 36:
        raise ValueError("base must be in [2, 36]")
    if n == 0:
        return "0"
    digits = []
    while n:
        n, r = divmod(n, base)
        digits.append(DIGITS[r])
    return "".join(reversed(digits))
