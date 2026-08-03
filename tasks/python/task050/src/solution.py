from __future__ import annotations

from collections import Counter


def unique_char_count(s: str) -> dict[str, int]:
    counts = Counter(s)
    return {ch: 1 for ch, cnt in counts.items() if cnt == 1}
