import re
from typing import Dict


def word_freq(text: str) -> Dict[str, int]:
    """
    Count frequency of words in the given text.

    A word is defined as a maximal run of Unicode letters and digits.
    All other characters (whitespace, punctuation, apostrophes, hyphens,
    underscores, etc.) act as separators. Matching is case-insensitive;
    words are lowercased before counting.

    Args:
        text: The input string to analyze.

    Returns:
        A dictionary mapping each lowercase word to its occurrence count.
        Returns an empty dict for empty or non-word-containing input.

    Raises:
        TypeError: If `text` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not text:
        return {}

    # [^\W_] matches any character that is a "word" character (\w) but not
    # an underscore. Since \w in Unicode mode covers letters, digits, and
    # underscore, excluding underscore leaves letters and digits only.
    pattern = re.compile(r'[^\W_]+', re.UNICODE)

    counts: Dict[str, int] = {}
    for match in pattern.finditer(text):
        word = match.group(0).lower()
        counts[word] = counts.get(word, 0) + 1

    return counts
