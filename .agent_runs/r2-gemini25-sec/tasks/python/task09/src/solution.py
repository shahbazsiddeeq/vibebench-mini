import collections
import re

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """
    Finds the top K most frequent words in a given text.

    The function processes the input text to extract alphanumeric words,
    counts their frequencies (case-insensitive), and returns the top K
    words along with their counts. Ties in frequency are broken by
    lexicographical order of the words (ascending).

    Args:
        text: The input string to analyze.
        k: The number of top frequent words to return. Must be a non-negative integer.

    Returns:
        A list of tuples, where each tuple contains a word (str) and its
        frequency (int), sorted by frequency (descending) and then by
        word (lexicographical ascending).

    Raises:
        ValueError: If k is negative or not an integer.
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    if not isinstance(k, int):
        raise ValueError("Input 'k' must be an integer.")
    if k < 0:
        raise ValueError("Input 'k' cannot be negative.")

    if not text or k == 0:
        return []

    # Use a regular expression to find sequences of alphanumeric characters.
    # This handles various delimiters and ensures only valid word characters are extracted.
    # Using re.findall is generally safer than split() for complex tokenization
    # as it explicitly defines what constitutes a token.
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())

    if not words:
        return []

    # Count word frequencies
    word_counts = collections.Counter(words)

    # Prepare for sorting:
    # Convert Counter items to a list of (word, count) tuples.
    # Sort criteria:
    # 1. Primary sort: by count (descending, hence -count)
    # 2. Secondary sort: by word (lexicographical ascending)
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

    # Return the top K elements
    return sorted_words[:k]
