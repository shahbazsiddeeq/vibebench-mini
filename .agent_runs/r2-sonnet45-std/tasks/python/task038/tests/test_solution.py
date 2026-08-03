import pytest
from src.solution import caesar


def test_basic_encode():
    assert caesar("Hello", 3) == "Khoor"


def test_preserves_case():
    assert caesar("ABC", 1) == "BCD"
    assert caesar("abc", 1) == "bcd"


def test_non_alpha_unchanged():
    assert caesar("Hello, World!", 3) == "Khoor, Zruog!"


def test_wraps_z():
    assert caesar("xyz", 3) == "abc"


def test_shift_zero():
    assert caesar("Hello", 0) == "Hello"


def test_shift_26():
    assert caesar("Hello", 26) == "Hello"


def test_negative_shift():
    assert caesar("Khoor", -3) == "Hello"


@pytest.mark.parametrize(
    "text,shift,expected",
    [
        ("ab", 25, "za"),
        ("Az", 1, "Ba"),
    ],
)
def test_parametrized(text, shift, expected):
    assert caesar(text, shift) == expected
