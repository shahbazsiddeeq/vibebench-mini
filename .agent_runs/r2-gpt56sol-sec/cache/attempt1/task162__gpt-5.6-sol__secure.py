"""Luhn checksum validation and check-digit generation."""


def _validate_digit_string(value: str) -> None:
    if not isinstance(value, str):
        raise TypeError("argument must be a string")
    if not value:
        raise ValueError("argument must not be empty")
    if any(character < "0" or character > "9" for character in value):
        raise ValueError("argument must contain only ASCII digits")


def luhn_valid(number: str) -> bool:
    """Return whether *number*, including its check digit, is Luhn-valid."""
    _validate_digit_string(number)

    total = 0
    for position, character in enumerate(reversed(number), start=1):
        digit = ord(character) - ord("0")
        if position % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


def luhn_check_digit(payload: str) -> int:
    """Return the Luhn check digit to append to *payload*."""
    _validate_digit_string(payload)

    total = 0
    # Once the check digit is appended, the payload's rightmost digit is at
    # position 2 and is therefore doubled.
    for position, character in enumerate(reversed(payload), start=1):
        digit = ord(character) - ord("0")
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return (-total) % 10
