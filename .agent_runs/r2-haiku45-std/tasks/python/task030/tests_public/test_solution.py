import pytest
from src.solution import word_freq


def test_empty():
    assert word_freq("") == {}


def test_punctuation_stripped():
    assert word_freq("hello, world!") == {"hello": 1, "world": 1}


def test_hyphenated_split():
    assert word_freq("state-of-the-art design") == {
        "state": 1,
        "of": 1,
        "the": 1,
        "art": 1,
        "design": 1,
    }


def test_digits_are_words():
    assert word_freq("abc 123 abc 123 abc") == {"abc": 3, "123": 2}


def test_single_word():
    assert word_freq("python") == {"python": 1}
