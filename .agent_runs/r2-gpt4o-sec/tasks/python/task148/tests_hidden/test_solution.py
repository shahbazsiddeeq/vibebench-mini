import pytest

from src.solution import parse_duration


def test_worked_example():
    assert parse_duration("1h30m") == 5400


def test_all_units():
    assert parse_duration("1w1d1h1m1s") == 604800 + 86400 + 3600 + 60 + 1


def test_zero_value():
    assert parse_duration("0m") == 0


def test_repeated_units_summed():
    assert parse_duration("1h1h") == 7200


def test_multi_digit():
    assert parse_duration("90m") == 5400


def test_bare_number_raises():
    with pytest.raises(ValueError):
        parse_duration("100")


def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("5y")


def test_whitespace_raises():
    with pytest.raises(ValueError):
        parse_duration("1h 30m")


def test_sign_raises():
    with pytest.raises(ValueError):
        parse_duration("-1h")


def test_returns_int_type():
    assert type(parse_duration("1m")) is int
