def reverse_words(s: str) -> str:
    # Split the string by whitespace and filter out any empty strings
    words = s.split()
    # Reverse the list of words
    reversed_words = words[::-1]
    # Join the reversed list with a single space
    return ' '.join(reversed_words)
