def validate_isbn13(isbn):
    cleaned = isbn.replace("-", "").replace(" ", "")

    if not cleaned.isdigit():
        raise ValueError("ISBN must contain only digits after stripping hyphens/spaces")

    if len(cleaned) != 13:
        raise ValueError("ISBN-13 must be exactly 13 digits long")

    total = 0
    for i, digit in enumerate(cleaned):
        n = int(digit)
        if i % 2 == 0:
            total += n
        else:
            total += n * 3

    return total % 10 == 0
