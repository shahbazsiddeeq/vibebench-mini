from collections import defaultdict
from typing import Iterable, List


def group_anagrams(words: Iterable[str]) -> List[List[str]]:
    groups = defaultdict(list)

    for word in words:
        groups["".join(sorted(word))].append(word)

    result = [sorted(group) for group in groups.values()]
    result.sort(key=lambda group: group[0])
    return result
