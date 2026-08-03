# src/solution.py

def validate_isbn13(isbn: str) -> bool:
    import re

    # Strip hyphens and spaces
    isbn_clean = re.sub(r'[-\s]', '', isbn)

    # Check for non-digit characters
    if not isbn_clean.isdigit():
        raise ValueError("ISBN contains non-digit characters after stripping.")

    # Check for correct length
    if len(isbn_clean) != 13:
        raise ValueError("ISBN must be 13 digits long.")

    # Calculate the checksum
    total = 0
    for i, char in enumerate(isbn_clean):
        digit = int(char)
        if i % 2 == 0:
            total += digit
        else:
            total += 3 * digit

    # Validate checksum
    return total % 10 == 0
