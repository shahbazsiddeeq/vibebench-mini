# src/solution.py

def reverse_words(s: str) -> str:
    # Split the string by whitespace and filter out empty strings
    words = s.split()
    # Reverse the list of words and join them with a single space
    return ' '.join(reversed(words))
