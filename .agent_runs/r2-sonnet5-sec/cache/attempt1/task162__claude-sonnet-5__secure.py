"""
Luhn mod-10 checksum utilities.

Provides:
    luhn_valid(number: str) -> bool
    luhn_check_digit(payload: str) -> int

Both functions validate their input strictly: the argument must be a
`str` containing only ASCII digit characters '0'-'9', and must not be
empty. Any violation raises TypeError (wrong type) or ValueError
(empty or invalid characters) without leaking internal details.
"""


def _validate_digit_string(value: str, name: str) -> None:
    """Validate that `value` is a non-empty string of ASCII digits.

    Raises:
        TypeError: if `value` is not a str.
        ValueError: if `value` is empty or contains non ASCII-digit
            characters.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str")
    if value == "":
        raise ValueError(f"{name} must not be empty")
    for ch in value:
        # Restrict strictly to ASCII '0'-'9'; reject unicode digits,
        # whitespace, signs, etc.
        if ch < "0" or ch > "9":
            raise ValueError(f"{name} must contain only ASCII digits 0-9")


def _luhn_sum(digits: str) -> int:
    """Compute the Luhn sum over a digit string, doubling every second
    digit counting from the rightmost digit (position 1)."""
    total = 0
    # Iterate from rightmost digit; double every second one.
    for index, ch in enumerate(reversed(digits)):
        d = ord(ch) - ord("0")
        if index % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def luhn_valid(number: str) -> bool:
    """Return True iff `number` (including its check digit) satisfies
    the Luhn checksum.

    Raises:
        TypeError: if `number` is not a str.
        ValueError: if `number` is empty or contains non-digit chars.
    """
    _validate_digit_string(number, "number")
    return _luhn_sum(number) % 10 == 0


def luhn_check_digit(payload: str) -> int:
    """Return the single check digit (0-9) that, appended to the
    right of `payload`, makes the resulting string Luhn-valid.

    Raises:
        TypeError: if `payload` is not a str.
        ValueError: if `payload` is empty or contains non-digit chars.
    """
    _validate_digit_string(payload, "payload")
    # The check digit occupies position 1 (rightmost) once appended,
    # so it is doubled with factor 1 (i.e., not doubled). We need
    # (sum_of_payload_with_shift + check_digit) % 10 == 0.
    # Payload digits shift by one position (their doubling parity
    # flips relative to the current unshifted computation), so we
    # compute the sum treating payload as if the check digit were 0,
    # then solve for the digit that zeroes the total mod 10.
    provisional_total = _luhn_sum(payload + "0")
    remainder = provisional_total % 10
    check_digit = (10 - remainder) % 10
    return check_digit
