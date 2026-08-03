from collections import defaultdict
from typing import Iterable


def group_anagrams(words: Iterable[str]) -> list[list[str]]:
    """Group anagram strings, sorting words and groups alphabetically."""
    if isinstance(words, (str, bytes)) or words is None:
        raise TypeError("words must be an iterable of strings")

    groups: dict[str, list[str]] = defaultdict(list)

    try:
        for word in words:
            if not isinstance(word, str):
                raise TypeError("all words must be strings")
            signature = "".join(sorted(word))
            groups[signature].append(word)
    except TypeError:
        raise
    except Exception as exc:
        raise ValueError("unable to process words") from exc

    result = [sorted(group) for group in groups.values()]
    result.sort(key=lambda group: group[0])
    return result
