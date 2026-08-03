import re
from collections import defaultdict


def word_freq(text: str) -> dict[str, int]:
    """
    Returns a dict mapping each lowercase word to the number of times it occurs.
    A word is a maximal run of Unicode letters and digits;
    every other character (whitespace, punctuation, apostrophes, hyphens,
    underscores) is a separator and is not part of a word. Matching is
    Unicode-aware, so accented words such as "café" stay intact, contractions
    like "don't" split into "don" and "t", and "state-of-the-art" splits into
    four words. Words are lowercased before counting; the empty string returns an
    empty dict.
    """
    if not text:
        return {}

    # Use re.findall with a Unicode-aware pattern for letters and digits.
    # The re.UNICODE flag (re.U) makes \w match Unicode word characters.
    # However, \w includes underscore, which we want to treat as a separator.
    # So, we explicitly define a word as a sequence of Unicode letters or digits.
    # \p{L} matches any kind of letter from any language.
    # \p{N} matches any kind of numeric character in any script.
    # The pattern `[\p{L}\p{N}]+` will match one or more Unicode letters or digits.
    # We need to compile the regex with re.UNICODE flag.
    word_pattern = re.compile(r'[\p{L}\p{N}]+', re.UNICODE)
    words = word_pattern.findall(text)

    frequency = defaultdict(int)
    for word in words:
        frequency[word.lower()] += 1

    return dict(frequency)
