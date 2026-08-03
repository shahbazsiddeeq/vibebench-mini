import re

def text_stats(text: str) -> dict:
    """
    Calculates various statistics for the given text.

    Args:
        text: The input string.

    Returns:
        A dictionary containing:
            - char_count (int): Total number of characters.
            - word_count (int): Number of whitespace-separated tokens.
            - sentence_count (int): Number of non-empty segments after splitting on sentence terminators.
            - avg_word_length (float): Mean length of words, rounded to 2 decimal places.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")

    char_count = len(text)
    words = text.split()
    word_count = len(words)

    # Calculate sentence count
    # Split on one or more occurrences of '.', '!', '?'
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings that might result from splitting (e.g., "Hello!!")
    sentence_count = len([s for s in sentences if s.strip()])

    total_word_length = sum(len(word) for word in words)
    avg_word_length = 0.0
    if word_count > 0:
        avg_word_length = round(total_word_length / word_count, 2)

    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
