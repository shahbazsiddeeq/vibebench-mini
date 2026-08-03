# src/solution.py

def unique_char_count(s: str) -> dict:
    char_count = {}
    
    # Count occurrences of each character
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    # Create a dictionary for unique characters
    unique_chars = {char: 1 for char, count in char_count.items() if count == 1}
    
    return unique_chars
