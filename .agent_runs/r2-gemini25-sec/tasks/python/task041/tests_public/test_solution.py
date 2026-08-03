from src.solution import longest_palindrome


def test_full_palindrome():
    assert longest_palindrome("racecar") == "racecar"


def test_two_same():
    assert longest_palindrome("aa") == "aa"


def test_empty():
    assert longest_palindrome("") == ""


def test_complex():
    result = longest_palindrome("abacaba")
    assert result == "abacaba"
