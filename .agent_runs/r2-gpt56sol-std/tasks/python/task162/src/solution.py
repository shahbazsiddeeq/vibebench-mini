def _validate_digits(value: str) -> None:
    if not isinstance(value, str):
        raise TypeError("number must be a string")
    if not value:
        raise ValueError("number must not be empty")
    if any(char < "0" or char > "9" for char in value):
        raise ValueError("number must contain only ASCII digits")


def luhn_valid(number: str) -> bool:
    _validate_digits(number)

    total = 0
    for position, char in enumerate(reversed(number), start=1):
        digit = ord(char) - ord("0")
        if position % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    _validate_digits(payload)

    total = 0
    for position, char in enumerate(reversed(payload), start=2):
        digit = ord(char) - ord("0")
        if position % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return (-total) % 10
