"""
src/solution.py

Top-K Frequent Words utility.

Provides `top_k_words(text, k)` which tokenizes input text into
case-insensitive alphanumeric words, counts their frequencies, and
returns the top-k most frequent words as a list of (word, count)
tuples. Ties are broken by lexicographic ascending order.

Security considerations:
- No use of eval/exec or dynamic code execution.
- Input types are strictly validated; invalid input raises TypeError
  or ValueError rather than causing unexpected behavior.
- No external I/O; function is pure and side-effect free.
- Regex used for tokenization is a simple, bounded pattern (no
  catastrophic backtracking risk) operating only on alnum characters.
"""

import re
from collections import Counter
from typing import List, Tuple

# Precompiled pattern: sequences of ASCII/unicode letters and digits.
_WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def top_k_words(text: str, k: int) -> List[Tuple[str, int]]:
    """
    Return the top-k most frequent alphanumeric words in `text`.

    Words are compared case-insensitively (lowercased). Ties in
    frequency are broken by ascending lexicographic order of the word.

    Args:
        text: Input string to analyze.
        k: Maximum number of (word, count) pairs to return. Must be
           a non-negative integer.

    Returns:
        A list of (word, count) tuples, sorted by descending count
        then ascending word, truncated to at most `k` entries.

    Raises:
        TypeError: if `text` is not a str or `k` is not an int.
        ValueError: if `k` is negative.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # bool is a subclass of int; explicitly reject it to avoid confusion.
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")

    if k < 0:
        raise ValueError("k must be non-negative")

    if not text or k == 0:
        return []

    words = _WORD_PATTERN.findall(text.lower())

    if not words:
        return []

    counts = Counter(words)

    # Sort by descending count, then ascending word (lexicographic).
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    return sorted_items[:k]
