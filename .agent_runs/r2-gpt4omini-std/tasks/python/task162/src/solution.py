def luhn_valid(number: str) -> bool:
    if not isinstance(number, str):
        raise TypeError("Input must be a string.")
    if not number or not number.isdigit():
        raise ValueError("Input must be a non-empty string of digits.")

    total = 0
    reverse_digits = number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Double every second digit
            n *= 2
            if n > 9:  # Subtract 9 from numbers over 9
                n -= 9
        total += n

    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    if not isinstance(payload, str):
        raise TypeError("Input must be a string.")
    if not payload or not payload.isdigit():
        raise ValueError("Input must be a non-empty string of digits.")

    total = 0
    reverse_digits = payload[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Double every second digit
            n *= 2
            if n > 9:  # Subtract 9 from numbers over 9
                n -= 9
        total += n

    # Calculate the check digit
    check_digit = (10 - (total % 10)) % 10
    return check_digit
