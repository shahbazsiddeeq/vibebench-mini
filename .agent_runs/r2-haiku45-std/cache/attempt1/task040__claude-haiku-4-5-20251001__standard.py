def to_roman(n):
    """
    Convert an integer (1-3999) to a Roman numeral string.
    
    Args:
        n: An integer between 1 and 3999 (inclusive)
        
    Returns:
        A string representing the Roman numeral
        
    Raises:
        ValueError: If n is not in the range 1-3999
    """
    if not isinstance(n, int) or n < 1 or n > 3999:
        raise ValueError(f"Number must be between 1 and 3999, got {n}")
    
    # Mapping of values to Roman numerals in descending order
    # Includes subtractive cases (like IV for 4, IX for 9, etc.)
    val_to_roman = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    ]
    
    result = []
    
    for value, numeral in val_to_roman:
        count = n // value
        if count:
            result.append(numeral * count)
            n -= value * count
    
    return ''.join(result)
