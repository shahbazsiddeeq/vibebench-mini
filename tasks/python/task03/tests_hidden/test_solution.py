from src.solution import is_palindrome


def test_basic():
    assert is_palindrome("level")


def test_negative():
    assert not is_palindrome("chatgpt 2025")


def test_single_char():
    assert is_palindrome("x")


def test_only_punctuation_reduces_to_empty():
    assert is_palindrome("!!! ...")
