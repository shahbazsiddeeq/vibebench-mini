from __future__ import annotations


class _TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "_TrieNode"] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
