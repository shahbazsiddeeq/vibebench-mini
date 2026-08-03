import pytest
from src.solution import word_wrap


def test_basic():
    assert word_wrap("the quick brown fox", 10) == ["the quick", "brown fox"]


def test_exact_fit():
    assert word_wrap("hello", 5) == ["hello"]


def test_long_word_raises():
    with pytest.raises(ValueError):
        word_wrap("superlongword", 5)


def test_single_word():
    assert word_wrap("python", 10) == ["python"]


def test_empty_string():
    assert word_wrap("", 10) == []


def test_multiple_spaces():
    assert word_wrap("a b c", 3) == ["a b", "c"]


def test_single_char_width():
    assert word_wrap("a b c", 1) == ["a", "b", "c"]


@pytest.mark.parametrize(
    "text,width,expected",
    [
        ("one two three", 7, ["one two", "three"]),
        ("hello world", 5, ["hello", "world"]),
    ],
)
def test_parametrized(text, width, expected):
    assert word_wrap(text, width) == expected


def test_boundary_line_not_over_width():
    # "abc de" would be length 6 (> 5) if the space is dropped from the
    # width check; the correct wrap breaks before "de".
    assert word_wrap("abc de fg", 5) == ["abc", "de fg"]


def test_no_returned_line_exceeds_width():
    cases = [
        ("the quick brown fox jumps over", 10),
        ("abc de fg hij", 5),
        ("aa bb cc dd ee ff", 4),
        ("one two three four five six", 7),
    ]
    for text, width in cases:
        for line in word_wrap(text, width):
            assert len(line) <= width, (text, width, line)
