# src/solution.py

def to_roman(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n < 1 or n > 3999:
        raise ValueError("Input must be between 1 and 3999.")

    roman_numerals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = []
    for value, numeral in roman_numerals:
        while n >= value:
            result.append(numeral)
            n -= value

    return ''.join(result)
