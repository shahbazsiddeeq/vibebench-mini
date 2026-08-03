import collections
import re

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """
    Finds the top-k most frequent words in a given text.

    The function processes the text to extract alphanumeric tokens,
    counts their frequencies (case-insensitive), and returns the top-k
    words along with their counts. Ties in frequency are broken by
    lexicographical order of the words (ascending).

    Args:
        text: The input string to analyze.
        k: The number of top frequent words to return.

    Returns:
        A list of tuples, where each tuple contains a word (str) and
        its frequency (int), sorted by frequency (descending) and then
        by word (lexicographically ascending) for ties.
    """
    if not text or k <= 0:
        return []

    # Use a regular expression to find alphanumeric tokens.
    # \b matches word boundaries, [a-zA-Z0-9]+ matches one or more
    # alphanumeric characters.
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

    if not words:
        return []

    # Count word frequencies
    word_counts = collections.Counter(words)

    # Sort the words based on frequency (descending) and then
    # lexicographically (ascending) for tie-breaking.
    # The key for sorting is a tuple: (-count, word).
    # -count ensures descending order for frequency.
    # word ensures ascending order for lexicographical tie-breaking.
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

    # Return the top k words
    return sorted_words[:k]
