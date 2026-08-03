from src.solution import reverse_words


def test_reverse_simple():
    assert reverse_words("hello world") == "world hello"


def test_reverse_single():
    assert reverse_words("hello") == "hello"


def test_whitespace_only():
    assert reverse_words("   ") == ""
    assert reverse_words("\t\n ") == ""


def test_tabs_and_newlines_are_separators():
    assert reverse_words("a\tb\nc") == "c b a"
