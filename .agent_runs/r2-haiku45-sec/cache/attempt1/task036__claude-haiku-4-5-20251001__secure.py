"""
Trie (Prefix Tree) implementation.

A Trie is a tree-like data structure that stores strings efficiently,
allowing fast prefix-based searches and word lookups.
"""


class TrieNode:
    """A single node in the Trie structure."""

    def __init__(self):
        """Initialize a TrieNode with empty children and is_word flag."""
        self.children = {}
        self.is_word = False


class Trie:
    """
    A Trie (Prefix Tree) data structure for efficient string storage and retrieval.

    Supports:
    - insert(word): Add a word to the trie
    - search(word): Check if a complete word exists
    - starts_with(prefix): Check if any word starts with the given prefix
    """

    def __init__(self):
        """Initialize an empty Trie with a root node."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Args:
            word: The word to insert. Must be a string.

        Raises:
            TypeError: If word is not a string.
            ValueError: If word is empty.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        if not word:
            raise ValueError("Word cannot be empty")

        node = self.root
        for char in word:
            # Validate character is a valid string character
            if not isinstance(char, str) or len(char) != 1:
                raise ValueError("Invalid character in word")

            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_word = True

    def search(self, word: str) -> bool:
        """
        Search for an exact word in the trie.

        Args:
            word: The word to search for. Must be a string.

        Returns:
            True if the word exists in the trie, False otherwise.

        Raises:
            TypeError: If word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")

        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.

        Args:
            prefix: The prefix to search for. Must be a string.

        Returns:
            True if any word starts with the prefix, False otherwise.

        Raises:
            TypeError: If prefix is not a string.
        """
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")

        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> TrieNode | None:
        """
        Find the node corresponding to the end of the given text.

        Args:
            text: The text to traverse (word or prefix).

        Returns:
            The TrieNode at the end of text, or None if text is not in the trie.
        """
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
