from src.solution import longest_palindrome


def test_basic_first_occurrence():
    # tie between "bab" and "aba"; the spec requires the first occurrence
    assert longest_palindrome("babad") == "bab"


def test_full_palindrome():
    assert longest_palindrome("racecar") == "racecar"


def test_single_char():
    assert longest_palindrome("a") == "a"


def test_two_same():
    assert longest_palindrome("aa") == "aa"


def test_two_different_first_occurrence():
    # all length-1 palindromes tie; first occurrence wins
    assert longest_palindrome("ab") == "a"


def test_empty():
    assert longest_palindrome("") == ""


def test_even_palindrome():
    assert longest_palindrome("cbbd") == "bb"


def test_complex():
    result = longest_palindrome("abacaba")
    assert result == "abacaba"
