import pytest
from src.solution import caesar


def test_basic_encode():
    assert caesar("Hello", 3) == "Khoor"


def test_non_alpha_unchanged():
    assert caesar("Hello, World!", 3) == "Khoor, Zruog!"


def test_shift_zero():
    assert caesar("Hello", 0) == "Hello"


def test_negative_shift():
    assert caesar("Khoor", -3) == "Hello"
