from __future__ import annotations

import re

WORD = re.compile(r"[^\W_]+", re.UNICODE)


def word_freq(text: str) -> dict[str, int]:
    words = WORD.findall(text.lower())
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq
