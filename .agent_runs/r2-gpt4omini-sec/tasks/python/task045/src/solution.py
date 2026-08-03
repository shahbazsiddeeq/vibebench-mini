# src/solution.py

def validate_isbn13(isbn: str) -> bool:
    # Remove hyphens and spaces
    sanitized_isbn = isbn.replace("-", "").replace(" ", "")
    
    # Validate length
    if len(sanitized_isbn) != 13:
        raise ValueError("ISBN must be 13 characters long after stripping.")
    
    # Validate that all characters are digits
    if not sanitized_isbn.isdigit():
        raise ValueError("ISBN must contain only digits after stripping.")
    
    # Calculate the checksum
    total = 0
    for i, digit in enumerate(sanitized_isbn):
        weight = 1 if i % 2 == 0 else 3
        total += int(digit) * weight
    
    # Validate checksum
    return total % 10 == 0
