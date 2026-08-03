from src.solution import top_k_words


def test_basic():
    s = "Red fish, blue fish; red RED!"
    assert top_k_words(s, 2) == [("red", 3), ("fish", 2)]


def test_k_zero():
    assert top_k_words("anything", 0) == []


def test_negative_k():
    assert top_k_words("a b c", -3) == []


def test_punctuation_stripped():
    s = "Hello, world! Hello... world? HELLO."
    assert top_k_words(s, 2) == [("hello", 3), ("world", 2)]
