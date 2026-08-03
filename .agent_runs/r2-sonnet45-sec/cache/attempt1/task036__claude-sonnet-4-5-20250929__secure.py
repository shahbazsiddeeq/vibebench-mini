class Trie:
    """A trie (prefix tree) data structure for efficient string storage and retrieval."""
    
    def __init__(self):
        """Initialize an empty trie with a root node."""
        self.root = {}
    
    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.
        
        Args:
            word: The word to insert. Must be a string.
        
        Raises:
            TypeError: If word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        # Mark end of word with a special key
        node['__end__'] = True
    
    def search(self, word: str) -> bool:
        """
        Search for an exact word in the trie.
        
        Args:
            word: The word to search for. Must be a string.
        
        Returns:
            True if the exact word exists in the trie, False otherwise.
        
        Raises:
            TypeError: If word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        # Check if this is marked as end of a word
        return '__end__' in node
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for. Must be a string.
        
        Returns:
            True if any word in the trie starts with the prefix, False otherwise.
        
        Raises:
            TypeError: If prefix is not a string.
        """
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")
        
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True
