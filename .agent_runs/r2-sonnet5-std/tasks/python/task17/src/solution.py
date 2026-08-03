import re
from typing import List, Tuple, Union

_TOKEN_RE = re.compile(r'\d+|\D+')

def _make_key(s: str) -> List[Tuple[int, Union[int, str]]]:
    key: List[Tuple[int, Union[int, str]]] = []
    for token in _TOKEN_RE.findall(s):
        if token[0].isdigit():
            key.append((0, int(token)))
        else:
            key.append((1, token))
    return key


def natural_sort(items: List[str]) -> List[str]:
    return sorted(items, key=_make_key)
