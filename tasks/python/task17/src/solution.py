import re
from typing import List, Tuple, Union

NUM = re.compile(r"\d+")


def _split_key(s: str) -> Tuple[Union[int, str], ...]:
    parts = []
    i = 0
    for m in NUM.finditer(s):
        if m.start() > i:
            parts.append(s[i : m.start()].lower())
        parts.append(int(m.group(0)))
        i = m.end()
    if i < len(s):
        parts.append(s[i:].lower())
    return tuple(parts)  # type: ignore[return-value]


def natural_sort(items: List[str]) -> List[str]:
    return sorted(items, key=_split_key)
