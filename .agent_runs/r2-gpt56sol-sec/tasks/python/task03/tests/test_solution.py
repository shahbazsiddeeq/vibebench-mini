from src.solution import is_palindrome


def test_basic():
    assert is_palindrome("level")


def test_case_space_punct():
    assert is_palindrome("A man, a plan, a canal: Panama")


def test_negative():
    assert not is_palindrome("chatgpt 2025")


def test_empty():
    assert is_palindrome("")


def test_single_char():
    assert is_palindrome("x")


def test_digits_only():
    assert is_palindrome("12321")
    assert not is_palindrome("12345")


def test_only_punctuation_reduces_to_empty():
    assert is_palindrome("!!! ...")


def test_non_ascii_stripped():
    # accented letters are non-ASCII and are ignored, so only "" remains
    assert is_palindrome("éàü")
    # "café" -> "caf", not a palindrome
    assert not is_palindrome("café")
