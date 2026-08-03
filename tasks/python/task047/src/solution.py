from __future__ import annotations

import re


def text_stats(text: str) -> dict:
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    sentences = re.split(r"[.!?]+", text)
    sentence_count = sum(1 for s in sentences if s.strip())
    avg_word_length = (
        round(sum(len(w) for w in words) / word_count, 2) if words else 0.0
    )
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
