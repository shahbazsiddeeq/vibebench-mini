"""Luhn mod-10 checksum: validation and check-digit computation."""

_DIGITS = frozenset("0123456789")


def _require_digits(s) -> None:
    if not isinstance(s, str):
        raise TypeError("argument must be str")
    if s == "":
        raise ValueError("argument must be non-empty")
    if not all(c in _DIGITS for c in s):
        raise ValueError("argument must contain only ASCII digits 0-9")


def _luhn_sum(number: str) -> int:
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = ord(ch) - 48
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def luhn_valid(number: str) -> bool:
    _require_digits(number)
    return _luhn_sum(number) % 10 == 0


def luhn_check_digit(payload: str) -> int:
    _require_digits(payload)
    # Appended digit occupies position 1 (rightmost, not doubled), which shifts
    # every existing digit's parity by one. Compute the sum of payload as if it
    # were shifted left by one position, then solve for the check digit.
    total = 0
    for i, ch in enumerate(reversed(payload)):
        d = ord(ch) - 48
        # existing digits move to positions 2,3,4,... so parity index is i+1
        if (i + 1) % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - (total % 10)) % 10
