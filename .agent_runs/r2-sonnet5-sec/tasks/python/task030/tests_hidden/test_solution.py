import pytest
from src.solution import word_freq


def test_basic():
    assert word_freq("hello world hello") == {"hello": 2, "world": 1}


def test_case_insensitive():
    assert word_freq("Hello HELLO hello") == {"hello": 3}


def test_contractions_split_on_apostrophe():
    assert word_freq("don't stop") == {"don": 1, "t": 1, "stop": 1}


def test_unicode_words_intact():
    assert word_freq("Café café CAFÉ") == {"café": 3}
    assert word_freq("naïve Straße") == {"naïve": 1, "straße": 1}


def test_underscore_is_separator():
    assert word_freq("foo_bar") == {"foo": 1, "bar": 1}


@pytest.mark.parametrize(
    "text,key,expected",
    [
        ("the cat sat on the mat", "the", 2),
        ("one two three two one", "two", 2),
    ],
)
def test_parametrized(text, key, expected):
    assert word_freq(text)[key] == expected
