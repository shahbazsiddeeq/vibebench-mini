import pytest
from src.solution import word_wrap


def test_basic():
    assert word_wrap("the quick brown fox", 10) == ["the quick", "brown fox"]


def test_long_word_raises():
    with pytest.raises(ValueError):
        word_wrap("superlongword", 5)


def test_empty_string():
    assert word_wrap("", 10) == []


def test_single_char_width():
    assert word_wrap("a b c", 1) == ["a", "b", "c"]


def test_boundary_line_not_over_width():
    # "abc de" would be length 6 (> 5) if the space is dropped from the
    # width check; the correct wrap breaks before "de".
    assert word_wrap("abc de fg", 5) == ["abc", "de fg"]
