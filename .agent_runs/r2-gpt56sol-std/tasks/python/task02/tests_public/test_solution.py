from src.solution import reverse_words


def test_reverse_trim():
    assert reverse_words(" a b c ") == "c b a"


def test_empty():
    assert reverse_words("") == ""


def test_multiple_spaces_collapsed():
    assert reverse_words("hello     world") == "world hello"


def test_leading_trailing_and_internal():
    assert reverse_words("  the   quick brown  ") == "brown quick the"
