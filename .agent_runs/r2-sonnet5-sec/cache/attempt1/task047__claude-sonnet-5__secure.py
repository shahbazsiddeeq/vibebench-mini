"""
src/solution.py

A small, security-conscious module that computes basic text statistics.

The function `text_stats` is intentionally simple and defensive:
    - It validates its input type explicitly (raising TypeError for
      non-string input) instead of silently coercing values, which could
      mask bugs or unexpected data from untrusted sources.
    - It performs no I/O, no eval/exec, and no use of external/untrusted
      code execution paths.
    - It only relies on the Python standard library.
"""

import re

# Precompile the sentence-splitting pattern once at import time.
# Splits on runs of '.', '!', or '?' characters.
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")


def text_stats(text: str) -> dict:
    """
    Compute basic statistics about the given text.

    Args:
        text: The input string to analyze.

    Returns:
        A dictionary with the following keys:
            - char_count (int): total number of characters (len(text)).
            - word_count (int): number of whitespace-separated tokens.
            - sentence_count (int): number of non-empty segments after
              splitting on runs of '.', '!', '?'.
            - avg_word_length (float): mean length of whitespace-separated
              words, rounded to 2 decimal places; 0.0 if there are no words.

    Raises:
        TypeError: if `text` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text_stats() expects a string input")

    char_count = len(text)

    words = text.split()
    word_count = len(words)

    # Split on runs of sentence-terminating punctuation and drop empty
    # segments (e.g., leading/trailing punctuation or consecutive marks).
    sentence_segments = _SENTENCE_SPLIT_RE.split(text)
    sentence_count = sum(1 for seg in sentence_segments if seg.strip() != "")

    if word_count > 0:
        total_length = sum(len(word) for word in words)
        avg_word_length = round(total_length / word_count, 2)
    else:
        avg_word_length = 0.0

    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
