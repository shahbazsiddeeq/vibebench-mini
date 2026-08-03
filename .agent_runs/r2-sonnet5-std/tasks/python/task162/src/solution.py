def _validate_str(value):
    if not isinstance(value, str):
        raise TypeError("Input must be a string")
    if len(value) == 0:
        raise ValueError("Input must not be empty")
    if not all(c in "0123456789" for c in value):
        raise ValueError("Input must contain only ASCII digits 0-9")


def luhn_valid(number: str) -> bool:
    _validate_str(number)
    total = 0
    digits = [int(c) for c in number]
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    _validate_str(payload)
    total = 0
    digits = [int(c) for c in payload]
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    remainder = total % 10
    return (10 - remainder) % 10
