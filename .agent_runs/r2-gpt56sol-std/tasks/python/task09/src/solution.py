import re
from collections import Counter


def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most frequent case-insensitive alphanumeric tokens."""
    if k <= 0:
        return []

    counts = Counter(re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE))
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]
