# src/solution.py

def reverse_words(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Split the string by whitespace and filter out empty strings
    words = s.split()
    
    # Reverse the list of words
    reversed_words = words[::-1]
    
    # Join the reversed list with a single space
    return ' '.join(reversed_words)
