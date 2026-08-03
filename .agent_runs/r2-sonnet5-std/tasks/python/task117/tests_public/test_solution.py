import pytest
from src.solution import int_to_base


def test_hex():
    assert int_to_base(255, 16) == "ff"


def test_zero():
    assert int_to_base(0, 10) == "0"


def test_negative():
    with pytest.raises(ValueError):
        int_to_base(-1, 10)
