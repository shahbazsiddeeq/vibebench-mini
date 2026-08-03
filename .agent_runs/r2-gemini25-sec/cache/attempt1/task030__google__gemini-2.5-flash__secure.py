import collections
import re

def word_freq(text: str) -> dict[str, int]:
    """
    Calculates the frequency of words in a given text.

    A word is defined as a maximal run of Unicode letters and digits.
    All other characters are considered separators. Words are converted
    to lowercase before counting.

    Args:
        text: The input string to analyze.

    Returns:
        A dictionary where keys are lowercase words and values are their
        respective frequencies. Returns an empty dictionary if the input
        text is empty or contains no words.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text:
        return {}

    # Use re.findall with a Unicode-aware pattern for letters and digits.
    # The re.UNICODE flag (re.U) is crucial for correct Unicode matching.
    # The pattern r'\b\w+\b' is often used, but \w includes underscore.
    # The task specifies "maximal run of Unicode letters and digits",
    # and "every other character ... is a separator".
    # So, we explicitly match Unicode letters (L) and digits (N).
    # \p{L} matches any kind of letter from any language.
    # \p{N} matches any kind of numeric character in any script.
    # The '+' quantifier ensures it's a maximal run.
    # re.IGNORECASE is not needed as we lowercase after extraction.
    words = re.findall(r'[\p{L}\p{N}]+', text, re.UNICODE)

    # Convert all extracted words to lowercase and count their frequencies
    word_counts = collections.defaultdict(int)
    for word in words:
        word_counts[word.lower()] += 1

    return dict(word_counts)
