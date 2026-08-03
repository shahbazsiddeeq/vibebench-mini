import secrets

def validate_isbn13(isbn: str) -> bool:
    """
    Validates an ISBN-13 string, including checksum verification.

    Args:
        isbn: The ISBN-13 string to validate. Can contain hyphens and spaces.

    Returns:
        True if the ISBN-13 is valid, False otherwise.

    Raises:
        ValueError: If the ISBN contains non-digit characters (after stripping
                    hyphens and spaces) or has an incorrect length (not 13 digits).
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string.")

    # Sanitize input: remove hyphens and spaces
    sanitized_isbn = isbn.replace('-', '').replace(' ', '')

    # Validate for non-digit characters
    if not sanitized_isbn.isdigit():
        raise ValueError("ISBN contains non-digit characters after stripping hyphens and spaces.")

    # Validate length
    if len(sanitized_isbn) != 13:
        raise ValueError(f"ISBN must be 13 digits long, but got {len(sanitized_isbn)} digits.")

    # Calculate checksum
    total_sum = 0
    for i, digit_char in enumerate(sanitized_isbn):
        digit = int(digit_char)
        if (i + 1) % 2 == 0:  # Even position (1-indexed) means odd index (0-indexed)
            total_sum += digit * 3
        else:  # Odd position (1-indexed) means even index (0-indexed)
            total_sum += digit * 1

    # The last digit of a valid ISBN-13 makes the total sum a multiple of 10.
    # So, total_sum % 10 should be 0 for a valid ISBN.
    return total_sum % 10 == 0
