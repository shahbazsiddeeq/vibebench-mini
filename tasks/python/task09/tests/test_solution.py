from src.solution import top_k_words


def test_basic():
    s = "Red fish, blue fish; red RED!"
    assert top_k_words(s, 2) == [("red", 3), ("fish", 2)]


def test_ties_lexicographic():
    s = "a b c b c"
    assert top_k_words(s, 3) == [("b", 2), ("c", 2), ("a", 1)]


def test_k_zero():
    assert top_k_words("anything", 0) == []
