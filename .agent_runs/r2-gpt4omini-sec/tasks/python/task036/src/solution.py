# src/solution.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        if not isinstance(word, str) or not word.isalpha():
            raise ValueError("Input must be a non-empty string containing only alphabetic characters.")
        
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True

    def search(self, word: str) -> bool:
        if not isinstance(word, str) or not word.isalpha():
            raise ValueError("Input must be a non-empty string containing only alphabetic characters.")
        
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        if not isinstance(prefix, str) or not prefix.isalpha():
            raise ValueError("Input must be a non-empty string containing only alphabetic characters.")
        
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True
