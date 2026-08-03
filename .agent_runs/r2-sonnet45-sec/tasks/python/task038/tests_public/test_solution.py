import pytest
from src.solution import caesar


def test_preserves_case():
    assert caesar("ABC", 1) == "BCD"
    assert caesar("abc", 1) == "bcd"


def test_wraps_z():
    assert caesar("xyz", 3) == "abc"


def test_shift_26():
    assert caesar("Hello", 26) == "Hello"


@pytest.mark.parametrize(
    "text,shift,expected",
    [
        ("ab", 25, "za"),
        ("Az", 1, "Ba"),
    ],
)
def test_parametrized(text, shift, expected):
    assert caesar(text, shift) == expected
