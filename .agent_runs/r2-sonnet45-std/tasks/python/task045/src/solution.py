def validate_isbn13(isbn):
    # Strip hyphens and spaces
    cleaned = isbn.replace('-', '').replace(' ', '')
    
    # Check if all characters are digits
    if not cleaned.isdigit():
        raise ValueError("ISBN contains non-digit characters")
    
    # Check length
    if len(cleaned) != 13:
        raise ValueError("ISBN must be exactly 13 digits")
    
    # Calculate checksum
    total = 0
    for i, digit in enumerate(cleaned):
        if i % 2 == 0:
            total += int(digit) * 1
        else:
            total += int(digit) * 3
    
    # Valid if checksum is divisible by 10
    return total % 10 == 0
