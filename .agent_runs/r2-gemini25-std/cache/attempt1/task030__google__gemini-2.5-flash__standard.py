import collections
import re


def word_freq(text: str) -> dict[str, int]:
    """
    Calculates the frequency of words in a given text.

    A word is defined as a maximal run of Unicode letters and digits.
    All other characters are considered separators. Words are converted
    to lowercase before counting.

    Args:
        text: The input string.

    Returns:
        A dictionary where keys are lowercase words and values are their
        respective frequencies.
    """
    if not text:
        return {}

    # Use a regular expression to find all sequences of Unicode letters or digits.
    # \p{L} matches any kind of letter from any language.
    # \p{N} matches any kind of numeric character in any script.
    # The re.UNICODE flag is crucial for correct Unicode matching.
    words = re.findall(r"[\p{L}\p{N}]+", text, re.UNICODE)

    # Convert all found words to lowercase and count their occurrences.
    word_counts = collections.defaultdict(int)
    for word in words:
        word_counts[word.lower()] += 1

    return dict(word_counts)
