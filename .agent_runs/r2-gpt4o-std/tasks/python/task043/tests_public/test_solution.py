import pytest
from src.solution import edit_distance


def test_empty_first():
    assert edit_distance("", "abc") == 3


def test_both_empty():
    assert edit_distance("", "") == 0


def test_single_insert():
    assert edit_distance("ab", "abc") == 1


def test_single_replace():
    assert edit_distance("abc", "axc") == 1
