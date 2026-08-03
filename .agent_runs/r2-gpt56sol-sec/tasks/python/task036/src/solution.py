"""Trie (prefix tree) implementation."""

from __future__ import annotations


class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    """A trie storing Unicode strings."""

    __slots__ = ("_root",)

    def __init__(self) -> None:
        self._root = _TrieNode()

    @staticmethod
    def _validate(value: str, name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        self._validate(word, "word")
        node = self._root

        for character in word:
            child = node.children.get(character)
            if child is None:
                child = _TrieNode()
                node.children[character] = child
            node = child

        node.is_word = True

    def search(self, word: str) -> bool:
        """Return whether an exact word exists in the trie."""
        self._validate(word, "word")
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Return whether any stored word starts with the given prefix."""
        self._validate(prefix, "prefix")
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> _TrieNode | None:
        node = self._root

        for character in text:
            node = node.children.get(character)
            if node is None:
                return None

        return node
