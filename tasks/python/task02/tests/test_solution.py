from src.solution import reverse_words


def test_reverse_simple():
    assert reverse_words("hello world") == "world hello"


def test_reverse_trim():
    assert reverse_words(" a b c ") == "c b a"


def test_reverse_single():
    assert reverse_words("hello") == "hello"


def test_empty():
    assert reverse_words("") == ""


def test_whitespace_only():
    assert reverse_words("   ") == ""
    assert reverse_words("\t\n ") == ""


def test_multiple_spaces_collapsed():
    assert reverse_words("hello     world") == "world hello"


def test_tabs_and_newlines_are_separators():
    assert reverse_words("a\tb\nc") == "c b a"


def test_leading_trailing_and_internal():
    assert reverse_words("  the   quick brown  ") == "brown quick the"
