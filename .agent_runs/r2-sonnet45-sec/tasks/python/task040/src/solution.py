def to_roman(n: int) -> str:
    """
    Convert an integer to a Roman numeral string.
    
    Args:
        n: Integer between 1 and 3999 (inclusive)
        
    Returns:
        Roman numeral representation as a string
        
    Raises:
        ValueError: If n is outside the range [1, 3999]
    """
    # Validate input type
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")
    
    # Validate input range
    if n < 1 or n > 3999:
        raise ValueError("Input must be between 1 and 3999 (inclusive)")
    
    # Mapping of values to Roman numerals in descending order
    # Including subtractive notation cases
    value_to_roman = [
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
        (1, 'I')
    ]
    
    result = []
    
    # Process each value-numeral pair
    for value, numeral in value_to_roman:
        count = n // value
        if count:
            result.append(numeral * count)
            n -= value * count
    
    return ''.join(result)
