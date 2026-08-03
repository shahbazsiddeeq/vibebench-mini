"""
ISBN-13 Validator

Provides validate_isbn13(isbn) which validates an ISBN-13 string against
the official checksum algorithm.

Security considerations:
- No use of eval/exec.
- No external randomness or I/O required.
- Strict input validation: only str input accepted, only digits (after
  stripping hyphens/spaces) allowed, exact length enforced.
- Error messages are generic and do not leak internal state.
"""

from typing import Union


def validate_isbn13(isbn: Union[str, bytes]) -> bool:
    """
    Validate an ISBN-13 string.

    The input may contain hyphens ('-') and spaces (' '), which are
    stripped before validation. After stripping, the resulting string
    must consist solely of exactly 13 ASCII digit characters, and must
    satisfy the ISBN-13 checksum algorithm.

    Args:
        isbn: The ISBN-13 string to validate.

    Returns:
        True if the ISBN-13 checksum is valid.

    Raises:
        ValueError: If the input is not a string, contains characters
            other than digits/hyphens/spaces, or does not have exactly
            13 digits after stripping.
    """
    if not isinstance(isbn, str):
        raise ValueError("Invalid ISBN-13 input")

    # Remove allowed separator characters only.
    cleaned = isbn.replace("-", "").replace(" ", "")

    if len(cleaned) != 13:
        raise ValueError("Invalid ISBN-13 input")

    if not cleaned.isdigit() or not cleaned.isascii():
        raise ValueError("Invalid ISBN-13 input")

    total = 0
    for index, char in enumerate(cleaned):
        digit = ord(char) - ord("0")
        weight = 1 if index % 2 == 0 else 3
        total += digit * weight

    return total % 10 == 0
