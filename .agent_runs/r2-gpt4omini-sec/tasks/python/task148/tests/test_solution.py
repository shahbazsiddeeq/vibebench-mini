import pytest

from src.solution import parse_duration


def test_worked_example():
    assert parse_duration("1h30m") == 5400


def test_days():
    assert parse_duration("2d") == 172800


def test_all_units():
    assert parse_duration("1w1d1h1m1s") == 604800 + 86400 + 3600 + 60 + 1


def test_single_second():
    assert parse_duration("45s") == 45


def test_zero_value():
    assert parse_duration("0m") == 0


def test_order_independent():
    assert parse_duration("30m1h") == 5400


def test_repeated_units_summed():
    assert parse_duration("1h1h") == 7200


def test_large_value():
    assert parse_duration("100h") == 360000


def test_multi_digit():
    assert parse_duration("90m") == 5400


def test_empty_raises():
    with pytest.raises(ValueError):
        parse_duration("")


def test_bare_number_raises():
    with pytest.raises(ValueError):
        parse_duration("100")


def test_unit_without_number_raises():
    with pytest.raises(ValueError):
        parse_duration("h")


def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("5y")


def test_uppercase_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("1H")


def test_whitespace_raises():
    with pytest.raises(ValueError):
        parse_duration("1h 30m")


def test_leading_space_raises():
    with pytest.raises(ValueError):
        parse_duration(" 1h")


def test_sign_raises():
    with pytest.raises(ValueError):
        parse_duration("-1h")


def test_decimal_raises():
    with pytest.raises(ValueError):
        parse_duration("1.5h")


def test_returns_int_type():
    assert type(parse_duration("1m")) is int


def test_mutation_killer_partial_match_rejected():
    # A solution using re.match/search instead of fullmatch would accept trailing junk.
    with pytest.raises(ValueError):
        parse_duration("1h30x")
