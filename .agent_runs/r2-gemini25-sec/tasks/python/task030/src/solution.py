import collections
import re

def word_freq(text: str) -> dict[str, int]:
    """
    Calculates the frequency of words in a given text.

    A word is defined as a maximal run of Unicode letters and digits.
    Other characters (whitespace, punctuation, etc.) are considered separators.
    Words are converted to lowercase before counting.

    Args:
        text: The input string.

    Returns:
        A dictionary where keys are lowercase words and values are their
        respective frequencies. Returns an empty dictionary if the input
        text is empty.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text:
        return {}

    # Use a regular expression to find all sequences of Unicode letters or digits.
    # \p{L} matches any kind of Unicode letter character.
    # \p{N} matches any kind of Unicode numeric character.
    # The re.UNICODE flag is crucial for correct Unicode matching.
    # The re.IGNORECASE flag is not used here because we lowercase words manually
    # after extraction to ensure consistent behavior across different regex engines
    # and to handle complex Unicode casing rules more predictably.
    words = re.findall(r'[\p{L}\p{N}]+', text, re.UNICODE)

    # Convert all extracted words to lowercase and count their frequencies.
    # Using collections.Counter is efficient for this task.
    return collections.Counter(word.lower() for word in words)
