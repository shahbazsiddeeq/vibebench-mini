"""Group Anagrams

Provides group_anagrams(words) which groups anagram words together.
Each group is sorted alphabetically and groups are ordered by their
first element.
"""

from collections import defaultdict
from typing import List


def group_anagrams(words: List[str]) -> List[List[str]]:
    """Group a list of words into anagram groups.

    Args:
        words: A list of strings to group.

    Returns:
        A list of lists, each containing words that are anagrams of
        each other, sorted alphabetically within each group, and the
        groups themselves sorted by their first element.

    Raises:
        TypeError: If ``words`` is not a list, or if any element of
            ``words`` is not a string.
    """
    if not isinstance(words, list):
        raise TypeError("words must be a list of strings")

    for item in words:
        if not isinstance(item, str):
            raise TypeError("all elements of words must be strings")

    if not words:
        return []

    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)

    result = []
    for key in groups:
        sorted_group = sorted(groups[key])
        result.append(sorted_group)

    result.sort(key=lambda g: g[0])

    return result
