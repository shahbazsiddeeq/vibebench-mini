class Trie:
    """
    A Trie (Prefix Tree) implementation for efficient word storage and retrieval.
    Supports inserting words, searching for words, and checking for prefixes.
    """

    def __init__(self):
        """
        Initializes an empty Trie.
        The root node is an empty dictionary.
        Each node in the Trie is a dictionary where keys are characters
        and values are child nodes. A special key '_end_' is used to mark
        the end of a word.
        """
        self._root = {}

    def _validate_input(self, word: str):
        """
        Validates the input word to ensure it's a non-empty string
        containing only lowercase English letters.

        Args:
            word: The string to validate.

        Raises:
            ValueError: If the word is not a string, is empty, or contains
                        invalid characters.
        """
        if not isinstance(word, str):
            raise ValueError("Input must be a string.")
        if not word:
            raise ValueError("Input string cannot be empty.")
        if not word.islower() or not word.isalpha():
            raise ValueError("Input string must contain only lowercase English letters.")

    def insert(self, word: str) -> None:
        """
        Inserts a word into the Trie.

        Args:
            word: The word to insert. Must be a non-empty string
                  containing only lowercase English letters.
        """
        try:
            self._validate_input(word)
        except ValueError as e:
            # Log the error or handle it as appropriate for the application.
            # For this problem, we'll re-raise or let it propagate as per typical
            # library behavior for invalid input.
            raise e

        current_node = self._root
        for char in word:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
        current_node['_end_'] = True  # Mark the end of a word

    def search(self, word: str) -> bool:
        """
        Searches for a word in the Trie.

        Args:
            word: The word to search for. Must be a non-empty string
                  containing only lowercase English letters.

        Returns:
            True if the word is found in the Trie, False otherwise.
        """
        try:
            self._validate_input(word)
        except ValueError:
            return False  # Invalid input means the word cannot be found

        current_node = self._root
        for char in word:
            if char not in current_node:
                return False
            current_node = current_node[char]
        return '_end_' in current_node

    def starts_with(self, prefix: str) -> bool:
        """
        Checks if there is any word in the Trie that starts with the given prefix.

        Args:
            prefix: The prefix to check. Must be a non-empty string
                    containing only lowercase English letters.

        Returns:
            True if any word in the Trie starts with the prefix, False otherwise.
        """
        try:
            self._validate_input(prefix)
        except ValueError:
            return False  # Invalid input means no word can start with this prefix

        current_node = self._root
        for char in prefix:
            if char not in current_node:
                return False
            current_node = current_node[char]
        return True
