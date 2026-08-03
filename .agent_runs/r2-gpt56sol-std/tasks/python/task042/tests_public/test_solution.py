import pytest
from src.solution import word_wrap


def test_exact_fit():
    assert word_wrap("hello", 5) == ["hello"]


def test_single_word():
    assert word_wrap("python", 10) == ["python"]


def test_multiple_spaces():
    assert word_wrap("a b c", 3) == ["a b", "c"]


@pytest.mark.parametrize(
    "text,width,expected",
    [
        ("one two three", 7, ["one two", "three"]),
        ("hello world", 5, ["hello", "world"]),
    ],
)
def test_parametrized(text, width, expected):
    assert word_wrap(text, width) == expected


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
