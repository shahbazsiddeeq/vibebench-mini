# src/solution.py

def validate_isbn13(isbn):
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # Check if the cleaned ISBN is exactly 13 characters long
    if len(isbn) != 13:
        raise ValueError("ISBN must be 13 digits long after stripping hyphens and spaces.")
    
    # Check if all characters are digits
    if not isbn.isdigit():
        raise ValueError("ISBN must contain only digits after stripping hyphens and spaces.")
    
    # Calculate the checksum using the ISBN-13 formula
    total = 0
    for i, char in enumerate(isbn):
        digit = int(char)
        if i % 2 == 0:
            total += digit
        else:
            total += 3 * digit
    
    # Valid ISBN-13 numbers have a total that is divisible by 10
    return total % 10 == 0
