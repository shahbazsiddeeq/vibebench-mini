# src/solution.py

def validate_isbn13(isbn):
    # Remove hyphens and spaces
    cleaned_isbn = isbn.replace('-', '').replace(' ', '')
    
    # Check for valid length
    if len(cleaned_isbn) != 13:
        raise ValueError("ISBN must be 13 characters long after stripping.")
    
    # Check for non-digit characters
    if not cleaned_isbn.isdigit():
        raise ValueError("ISBN must contain only digits after stripping.")
    
    # Calculate the checksum
    total = 0
    for i, digit in enumerate(cleaned_isbn):
        weight = 1 if i % 2 == 0 else 3
        total += int(digit) * weight
    
    # Validate the checksum
    return total % 10 == 0
