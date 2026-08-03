import pytest
from src.solution import to_roman


def test_one():
    assert to_roman(1) == "I"


def test_four():
    assert to_roman(4) == "IV"


def test_nine():
    assert to_roman(9) == "IX"


def test_fourteen():
    assert to_roman(14) == "XIV"


def test_forty():
    assert to_roman(40) == "XL"


def test_1994():
    assert to_roman(1994) == "MCMXCIV"


def test_3999():
    assert to_roman(3999) == "MMMCMXCIX"


def test_zero_raises():
    with pytest.raises(ValueError):
        to_roman(0)


def test_4000_raises():
    with pytest.raises(ValueError):
        to_roman(4000)


@pytest.mark.parametrize(
    "n,expected",
    [
        (58, "LVIII"),
        (3, "III"),
        (400, "CD"),
    ],
)
def test_parametrized(n, expected):
    assert to_roman(n) == expected
