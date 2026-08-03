from src.solution import Trie


def test_insert_search_found():
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True


def test_search_not_found():
    t = Trie()
    t.insert("apple")
    assert t.search("app") is False


def test_starts_with_true():
    t = Trie()
    t.insert("apple")
    assert t.starts_with("app") is True


def test_starts_with_false():
    t = Trie()
    t.insert("apple")
    assert t.starts_with("ban") is False


def test_empty_prefix():
    t = Trie()
    t.insert("hello")
    assert t.starts_with("") is True


def test_overlapping_words():
    t = Trie()
    t.insert("app")
    t.insert("apple")
    assert t.search("app") is True
    assert t.search("apple") is True
    assert t.starts_with("appl") is True


def test_search_after_multiple_inserts():
    t = Trie()
    for w in ["cat", "car", "card", "care"]:
        t.insert(w)
    assert t.search("car") is True
    assert t.search("ca") is False
    assert t.starts_with("car") is True


def test_independent_tries():
    # Two tries must not share state (e.g. a single class-level root).
    t1 = Trie()
    t2 = Trie()
    t1.insert("apple")
    assert t2.search("apple") is False
    assert t2.starts_with("app") is False
    t2.insert("banana")
    assert t1.search("banana") is False
    assert t1.starts_with("ban") is False
    assert t1.search("apple") is True
    assert t2.search("banana") is True
