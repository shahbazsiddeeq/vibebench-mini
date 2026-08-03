import pytest
from src.solution import is_balanced


def test_empty_string():
    assert is_balanced("") is True


def test_nested():
    assert is_balanced("([{}])") is True


def test_unmatched_open():
    assert is_balanced("((") is False


def test_wrong_close():
    assert is_balanced("(]") is False


def test_deeply_nested():
    assert is_balanced("(" * 1000 + ")" * 1000) is True
    assert is_balanced("([{" * 500 + "}])" * 500) is True
    assert is_balanced("(" * 1000 + ")" * 999) is False
    assert is_balanced("[" + "([{}])" * 500 + "]") is True
