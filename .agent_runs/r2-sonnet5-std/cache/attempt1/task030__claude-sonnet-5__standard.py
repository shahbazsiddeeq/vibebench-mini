import re

_WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


def word_freq(text):
    """Return a dict mapping each lowercase word to its frequency count.

    A word is a maximal run of Unicode letters and digits; all other
    characters (whitespace, punctuation, apostrophes, hyphens, underscores)
    act as separators.
    """
    freq = {}
    for match in _WORD_RE.findall(text):
        word = match.lower()
        freq[word] = freq.get(word, 0) + 1
    return freq
