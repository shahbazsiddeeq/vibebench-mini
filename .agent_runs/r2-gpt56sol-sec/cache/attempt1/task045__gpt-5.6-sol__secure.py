"""ISBN-13 validation utilities."""


def validate_isbn13(isbn: str) -> bool:
    """Return whether *isbn* has a valid ISBN-13 checksum.

    Spaces and hyphens are removed before validation.

    Raises:
        ValueError: If the input is not a string, contains other characters,
            or does not contain exactly 13 digits after normalization.
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string")

    normalized = isbn.replace(" ", "").replace("-", "")

    if len(normalized) != 13:
        raise ValueError("ISBN must contain exactly 13 digits")
    if not normalized.isascii() or not normalized.isdigit():
        raise ValueError("ISBN must contain only digits, spaces, and hyphens")

    checksum = sum(
        int(digit) * (1 if index % 2 == 0 else 3)
        for index, digit in enumerate(normalized)
    )
    return checksum % 10 == 0
