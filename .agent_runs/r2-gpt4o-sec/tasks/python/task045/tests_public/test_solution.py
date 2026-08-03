import pytest
from src.solution import validate_isbn13


def test_valid_plain():
    assert validate_isbn13("9783161484100") is True


def test_wrong_length_raises():
    with pytest.raises(ValueError):
        validate_isbn13("12345")


def test_valid_with_spaces():
    assert validate_isbn13("978 3 16 148410 0") is True
