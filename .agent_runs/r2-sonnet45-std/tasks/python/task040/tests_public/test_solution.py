import pytest
from src.solution import to_roman


def test_four():
    assert to_roman(4) == "IV"


def test_fourteen():
    assert to_roman(14) == "XIV"


def test_1994():
    assert to_roman(1994) == "MCMXCIV"


def test_zero_raises():
    with pytest.raises(ValueError):
        to_roman(0)


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
