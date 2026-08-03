class Trie:
    def __init__(self):
        self.root = {}
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        # Mark end of word with a special key
        node['$'] = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        # Check if this is marked as end of a word
        return '$' in node
    
    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True
