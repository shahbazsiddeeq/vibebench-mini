from src.solution import top_k_words


def test_ties_lexicographic():
    s = "a b c b c"
    assert top_k_words(s, 3) == [("b", 2), ("c", 2), ("a", 1)]


def test_k_larger_than_word_count():
    assert top_k_words("a b c", 10) == [("a", 1), ("b", 1), ("c", 1)]


def test_empty_text():
    assert top_k_words("", 5) == []
