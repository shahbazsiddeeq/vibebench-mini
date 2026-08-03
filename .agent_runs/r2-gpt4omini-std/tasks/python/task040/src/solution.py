# src/solution.py

def to_roman(n):
    if not (1 <= n <= 3999):
        raise ValueError("Input must be between 1 and 3999")

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    
    roman_num = ""
    for i in range(len(val)):
        while n >= val[i]:
            roman_num += syms[i]
            n -= val[i]
    return roman_num
