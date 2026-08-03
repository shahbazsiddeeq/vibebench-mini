class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self._root
        for char in word:
            node = node.children.setdefault(char, _TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> _TrieNode | None:
        node = self._root
        for char in text:
            node = node.children.get(char)
            if node is None:
                return None
        return node
