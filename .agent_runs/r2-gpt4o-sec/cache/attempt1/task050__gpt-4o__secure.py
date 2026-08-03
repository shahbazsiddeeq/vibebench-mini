# src/solution.py

def unique_char_count(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    char_count = {}
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    unique_chars = {char: 1 for char in s if char_count[char] == 1}
    
    return unique_chars
