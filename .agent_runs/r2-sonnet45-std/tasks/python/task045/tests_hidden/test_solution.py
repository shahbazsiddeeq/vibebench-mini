import pytest
from src.solution import validate_isbn13


def test_valid_with_hyphens():
    assert validate_isbn13("978-3-16-148410-0") is True


def test_invalid_checksum():
    assert validate_isbn13("9783161484101") is False


def test_non_digit_raises():
    with pytest.raises(ValueError):
        validate_isbn13("97831614841XX")


@pytest.mark.parametrize(
    "isbn,expected",
    [
        ("9780306406157", True),
        ("9780306406158", False),
    ],
)
def test_parametrized(isbn, expected):
    assert validate_isbn13(isbn) == expected
