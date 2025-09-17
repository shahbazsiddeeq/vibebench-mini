from src.solution import is_palindrome


def test_basic():
    assert is_palindrome("level")


def test_case_space_punct():
    assert is_palindrome("A man, a plan, a canal: Panama")


def test_negative():
    assert not is_palindrome("chatgpt 2025")
