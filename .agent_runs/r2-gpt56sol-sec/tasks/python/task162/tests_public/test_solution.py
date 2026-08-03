import pytest

from src.solution import luhn_valid, luhn_check_digit


def test_known_invalid_last_digit():
    assert luhn_valid("79927398710") is False


def test_check_digit_completes_to_valid():
    payload = "7992739871"
    cd = luhn_check_digit(payload)
    assert luhn_valid(payload + str(cd)) is True


def test_check_digit_zero_case():
    # A payload whose completing check digit is 0.
    assert luhn_check_digit("123456781234567") == 0


def test_mutation_only_last_digit_flips_validity():
    # Exactly one of the ten single-check-digit completions is valid.
    base = "7992739871"
    valid = [d for d in range(10) if luhn_valid(base + str(d))]
    assert valid == [3]


def test_empty_raises():
    with pytest.raises(ValueError):
        luhn_valid("")
    with pytest.raises(ValueError):
        luhn_check_digit("")
