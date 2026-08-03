"""Simultaneous string replacement utilities."""

from collections.abc import Mapping
from typing import Any


def find_replace(text: str, replacements: Mapping[str, str]) -> str:
    """
    Apply replacements simultaneously to *text*.

    Matching is performed against the original text from left to right. When
    multiple keys match at the same position, the longest key takes priority.
    Replacement results are not searched again.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(replacements, Mapping):
        raise TypeError("replacements must be a mapping")

    items = list(replacements.items())
    if not items:
        return text

    terminal = object()
    trie: dict[Any, Any] = {}

    for key, value in items:
        if not isinstance(key, str):
            raise TypeError("replacement keys must be strings")
        if not isinstance(value, str):
            raise TypeError("replacement values must be strings")
        if not key:
            raise ValueError("replacement keys must not be empty")

        node = trie
        for character in key:
            node = node.setdefault(character, {})
        node[terminal] = value

    result: list[str] = []
    position = 0
    text_length = len(text)

    while position < text_length:
        node = trie
        cursor = position
        matched_end = -1
        matched_value: str | None = None

        while cursor < text_length:
            next_node = node.get(text[cursor])
            if next_node is None:
                break

            node = next_node
            cursor += 1

            if terminal in node:
                matched_end = cursor
                matched_value = node[terminal]

        if matched_end >= 0:
            result.append(matched_value if matched_value is not None else "")
            position = matched_end
        else:
            result.append(text[position])
            position += 1

    return "".join(result)
