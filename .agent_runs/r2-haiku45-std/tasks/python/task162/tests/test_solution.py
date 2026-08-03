import pytest

from src.solution import luhn_valid, luhn_check_digit


def test_known_valid():
    assert luhn_valid("79927398713") is True


def test_known_invalid_last_digit():
    assert luhn_valid("79927398710") is False


def test_check_digit_classic():
    assert luhn_check_digit("7992739871") == 3


def test_check_digit_completes_to_valid():
    payload = "7992739871"
    cd = luhn_check_digit(payload)
    assert luhn_valid(payload + str(cd)) is True


def test_more_valid_numbers():
    assert luhn_valid("4532015112830366") is True
    assert luhn_valid("1234567812345670") is True


def test_check_digit_zero_case():
    # A payload whose completing check digit is 0.
    assert luhn_check_digit("123456781234567") == 0


def test_single_digit_valid():
    assert luhn_valid("0") is True
    assert luhn_valid("5") is False


def test_mutation_only_last_digit_flips_validity():
    # Exactly one of the ten single-check-digit completions is valid.
    base = "7992739871"
    valid = [d for d in range(10) if luhn_valid(base + str(d))]
    assert valid == [3]


def test_type_errors():
    with pytest.raises(TypeError):
        luhn_valid(79927398713)
    with pytest.raises(TypeError):
        luhn_check_digit(7992739871)


def test_empty_raises():
    with pytest.raises(ValueError):
        luhn_valid("")
    with pytest.raises(ValueError):
        luhn_check_digit("")


def test_non_digit_raises():
    with pytest.raises(ValueError):
        luhn_valid("7992 7398 713")
    with pytest.raises(ValueError):
        luhn_valid("-123")
    with pytest.raises(ValueError):
        # Unicode digit (Arabic-Indic 5) must be rejected.
        luhn_valid("1234٥")
