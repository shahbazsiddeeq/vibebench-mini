"""Utilities for calculating text statistics."""

import re
from typing import Dict, Union

_SENTENCE_DELIMITERS = re.compile(r"[.!?]+")


def text_stats(text: str) -> Dict[str, Union[int, float]]:
    """Return character, word, sentence, and average word-length statistics."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    words = text.split()
    word_count = len(words)

    segments = _SENTENCE_DELIMITERS.split(text)
    sentence_count = sum(1 for segment in segments if segment.strip())

    avg_word_length = (
        round(sum(len(word) for word in words) / word_count, 2)
        if word_count
        else 0.0
    )

    return {
        "char_count": len(text),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
