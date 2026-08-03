import pytest
from src.solution import edit_distance


def test_identical():
    assert edit_distance("abc", "abc") == 0


def test_empty_first():
    assert edit_distance("", "abc") == 3


def test_empty_second():
    assert edit_distance("abc", "") == 3


def test_both_empty():
    assert edit_distance("", "") == 0


def test_classic():
    assert edit_distance("kitten", "sitting") == 3


def test_single_insert():
    assert edit_distance("ab", "abc") == 1


def test_single_delete():
    assert edit_distance("abc", "ab") == 1


def test_single_replace():
    assert edit_distance("abc", "axc") == 1


@pytest.mark.parametrize(
    "s1,s2,expected",
    [
        ("sunday", "saturday", 3),
        ("horse", "ros", 3),
    ],
)
def test_parametrized(s1, s2, expected):
    assert edit_distance(s1, s2) == expected
