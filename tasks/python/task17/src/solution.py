import re
from typing import List, Tuple

NUM = re.compile(r"\d+")


def _split_key(s: str) -> Tuple[tuple, ...]:
    # Each chunk is tagged with a type marker (0 = numeric, 1 = text) so that a
    # digit run and a letter run at the same position never compare int-vs-str
    # (which would raise TypeError). Numeric chunks sort before text chunks.
    parts = []
    i = 0
    for m in NUM.finditer(s):
        if m.start() > i:
            parts.append((1, s[i : m.start()]))
        parts.append((0, int(m.group(0))))
        i = m.end()
    if i < len(s):
        parts.append((1, s[i:]))
    return tuple(parts)


def natural_sort(items: List[str]) -> List[str]:
    return sorted(items, key=_split_key)
