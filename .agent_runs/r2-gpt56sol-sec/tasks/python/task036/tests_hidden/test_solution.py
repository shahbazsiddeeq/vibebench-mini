from src.solution import Trie


def test_insert_search_found():
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True


def test_starts_with_true():
    t = Trie()
    t.insert("apple")
    assert t.starts_with("app") is True


def test_empty_prefix():
    t = Trie()
    t.insert("hello")
    assert t.starts_with("") is True


def test_search_after_multiple_inserts():
    t = Trie()
    for w in ["cat", "car", "card", "care"]:
        t.insert(w)
    assert t.search("car") is True
    assert t.search("ca") is False
    assert t.starts_with("car") is True
