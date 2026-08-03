def validate_isbn13(isbn):
    """Return whether *isbn* has a valid ISBN-13 checksum.

    Hyphens and whitespace are ignored. A ValueError is raised if the
    normalized value is not exactly 13 digits.
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string")

    normalized = "".join(char for char in isbn if char != "-" and not char.isspace())

    if len(normalized) != 13:
        raise ValueError("ISBN-13 must contain exactly 13 digits")
    if not normalized.isascii() or not normalized.isdigit():
        raise ValueError("ISBN-13 must contain only digits, hyphens, and spaces")

    digits = [int(char) for char in normalized]
    checksum = sum(
        digit if index % 2 == 0 else digit * 3
        for index, digit in enumerate(digits)
    )
    return checksum % 10 == 0
