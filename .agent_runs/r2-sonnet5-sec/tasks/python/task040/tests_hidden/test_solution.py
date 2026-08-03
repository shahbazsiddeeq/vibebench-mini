import pytest
from src.solution import to_roman


def test_one():
    assert to_roman(1) == "I"


def test_nine():
    assert to_roman(9) == "IX"


def test_forty():
    assert to_roman(40) == "XL"


def test_3999():
    assert to_roman(3999) == "MMMCMXCIX"


def test_4000_raises():
    with pytest.raises(ValueError):
        to_roman(4000)
