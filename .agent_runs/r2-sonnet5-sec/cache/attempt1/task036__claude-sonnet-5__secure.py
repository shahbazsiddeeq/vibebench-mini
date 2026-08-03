"""
A secure, self-contained implementation of a Trie (Prefix Tree).

This module provides a `Trie` class supporting:
    - insert(word: str) -> None
    - search(word: str) -> bool
    - starts_with(prefix: str) -> bool

Design notes / security considerations:
    - All public methods strictly validate their inputs are `str` instances,
      raising `TypeError` otherwise. This avoids silently mis-processing
      unexpected types (e.g., bytes, None, numbers) which could lead to
      confusing behavior or injection-like issues downstream.
    - No use of eval/exec or any dynamic code execution.
    - No I/O operations are performed (no file, network, or subprocess use).
    - Randomness is not required for this data structure, so the `secrets`
      module is not applicable here; no insecure `random` usage is present.
    - Each `Trie` instance owns its own root node, ensuring no shared
      mutable state between separate instances.
    - Internal errors (e.g., programming bugs) are not exposed to callers;
      only well-defined `TypeError` is raised for invalid input types, and
      no internal state or stack traces are leaked.
"""

from typing import Dict, Optional


class _TrieNode:
    """Internal node representation for the Trie.

    Not intended for external use.
    """

    __slots__ = ("children", "is_end_of_word")

    def __init__(self) -> None:
        self.children: Dict[str, "_TrieNode"] = {}
        self.is_end_of_word: bool = False


class Trie:
    """A prefix tree (Trie) supporting insert, search, and prefix search.

    Each instance maintains its own independent root node, so multiple
    `Trie` instances do not share state.
    """

    def __init__(self) -> None:
        self._root: _TrieNode = _TrieNode()

    @staticmethod
    def _validate_word(word: str) -> str:
        """Validate that `word` is a string; return it unchanged.

        Raises:
            TypeError: if `word` is not a `str`.
        """
        if not isinstance(word, str):
            raise TypeError("word must be a string")
        return word

    def insert(self, word: str) -> None:
        """Insert `word` into the trie.

        Args:
            word: The word to insert. Must be a `str` (may be empty).

        Raises:
            TypeError: if `word` is not a string.
        """
        word = self._validate_word(word)

        node = self._root
        for char in word:
            next_node = node.children.get(char)
            if next_node is None:
                next_node = _TrieNode()
                node.children[char] = next_node
            node = next_node
        node.is_end_of_word = True

    def _find_node(self, prefix: str) -> Optional[_TrieNode]:
        """Return the node corresponding to the end of `prefix`, or None."""
        node = self._root
        for char in prefix:
            next_node = node.children.get(char)
            if next_node is None:
                return None
            node = next_node
        return node

    def search(self, word: str) -> bool:
        """Return True if `word` was previously inserted exactly.

        Args:
            word: The word to search for. Must be a `str`.

        Returns:
            bool: True if the exact word exists in the trie, False otherwise.

        Raises:
            TypeError: if `word` is not a string.
        """
        word = self._validate_word(word)
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Return True if any inserted word starts with `prefix`.

        Args:
            prefix: The prefix to check. Must be a `str`.

        Returns:
            bool: True if some word in the trie starts with `prefix`.

        Raises:
            TypeError: if `prefix` is not a string.
        """
        prefix = self._validate_word(prefix)
        return self._find_node(prefix) is not None
