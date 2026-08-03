from src.solution import top_k_words


def test_basic():
    s = "Red fish, blue fish; red RED!"
    assert top_k_words(s, 2) == [("red", 3), ("fish", 2)]


def test_ties_lexicographic():
    s = "a b c b c"
    assert top_k_words(s, 3) == [("b", 2), ("c", 2), ("a", 1)]


def test_k_zero():
    assert top_k_words("anything", 0) == []


def test_k_larger_than_word_count():
    assert top_k_words("a b c", 10) == [("a", 1), ("b", 1), ("c", 1)]


def test_negative_k():
    assert top_k_words("a b c", -3) == []


def test_empty_text():
    assert top_k_words("", 5) == []


def test_punctuation_stripped():
    s = "Hello, world! Hello... world? HELLO."
    assert top_k_words(s, 2) == [("hello", 3), ("world", 2)]
