# src/solution.py

def unique_char_count(s):
    from collections import Counter
    
    # Count occurrences of each character
    char_count = Counter(s)
    
    # Create a dictionary for characters that appear exactly once
    unique_chars = {char: 1 for char in s if char_count[char] == 1}
    
    return unique_chars
