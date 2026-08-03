class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.END_OF_WORD = '#'

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node[self.END_OF_WORD] = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        node = self._traverse(word)
        return node is not None and self.END_OF_WORD in node

    def starts_with(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        return self._traverse(prefix) is not None

    def _traverse(self, prefix: str) -> dict:
        """
        Helper function to traverse the trie.
        Returns the node corresponding to the end of the prefix, or None if not found.
        """
        node = self.root
        for char in prefix:
            if char not in node:
                return None
            node = node[char]
        return node
