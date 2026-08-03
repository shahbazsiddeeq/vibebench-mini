def validate_isbn13(isbn: str) -> bool:
    """
    Validates an ISBN-13 string.

    The function first strips hyphens and spaces from the input string.
    It then checks for non-digit characters and correct length (13 digits).
    Finally, it performs the ISBN-13 checksum validation.

    Args:
        isbn: The ISBN-13 string to validate.

    Returns:
        True if the ISBN-13 is valid, False otherwise.

    Raises:
        ValueError: If the ISBN contains non-digit characters (after stripping)
                    or if its length is not 13 digits.
    """
    cleaned_isbn = isbn.replace("-", "").replace(" ", "")

    if not cleaned_isbn.isdigit():
        raise ValueError("ISBN must contain only digits (after stripping hyphens and spaces).")

    if len(cleaned_isbn) != 13:
        raise ValueError("ISBN must be 13 digits long.")

    total_sum = 0
    for i, digit_char in enumerate(cleaned_isbn):
        digit = int(digit_char)
        if i % 2 == 0:  # Odd position (1st, 3rd, etc.)
            total_sum += digit
        else:  # Even position (2nd, 4th, etc.)
            total_sum += digit * 3

    return total_sum % 10 == 0
