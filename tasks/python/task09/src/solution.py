import re
from collections import Counter
from typing import List, Tuple

WORD = re.compile(r"[A-Za-z0-9]+")


def top_k_words(text: str, k: int) -> List[Tuple[str, int]]:
    tokens = [t.lower() for t in WORD.findall(text)]
    counts = Counter(tokens)
    items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return items[: max(0, k)]
