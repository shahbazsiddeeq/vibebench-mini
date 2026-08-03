import pytest
from src.solution import lcs_length


def test_classic():
    assert lcs_length("ABCBDAB", "BDCAB") == 4


def test_no_common():
    assert lcs_length("ABC", "DEF") == 0


def test_empty_second():
    assert lcs_length("ABC", "") == 0


def test_single_char_match():
    assert lcs_length("A", "A") == 1


@pytest.mark.parametrize(
    "s1,s2,expected",
    [
        ("AGGTAB", "GXTXAYB", 4),
        ("ABAB", "BABA", 3),
    ],
)
def test_parametrized(s1, s2, expected):
    assert lcs_length(s1, s2) == expected
