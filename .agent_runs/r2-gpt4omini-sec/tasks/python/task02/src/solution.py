# src/solution.py

def reverse_words(s: str) -> str:
    # Validate input type
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Strip leading/trailing whitespace and split by whitespace
    words = s.strip().split()
    
    # Reverse the list of words
    reversed_words = words[::-1]
    
    # Join the reversed words with a single space
    return ' '.join(reversed_words)
