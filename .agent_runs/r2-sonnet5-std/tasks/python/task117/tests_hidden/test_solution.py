import pytest
from src.solution import int_to_base


def test_binary():
    assert int_to_base(10, 2) == "1010"


def test_octal():
    assert int_to_base(8, 8) == "10"


def test_base36():
    assert int_to_base(35, 36) == "z"


def test_invalid_base():
    with pytest.raises(ValueError):
        int_to_base(10, 1)
    with pytest.raises(ValueError):
        int_to_base(10, 37)
