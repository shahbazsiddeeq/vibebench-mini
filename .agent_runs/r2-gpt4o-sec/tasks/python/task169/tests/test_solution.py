import pytest

from src.solution import parse_accept_language


def test_basic_sorted_desc():
    assert parse_accept_language("en-US,en;q=0.9,fr;q=0.8") == [
        ("en-us", 1.0),
        ("en", 0.9),
        ("fr", 0.8),
    ]


def test_default_quality_is_one():
    assert parse_accept_language("de") == [("de", 1.0)]


def test_reorders_by_quality():
    # Mutation killer: a parser that skips sorting returns input order
    # [('a',0.5),('b',1.0)] instead of the quality-sorted result.
    assert parse_accept_language("a;q=0.5,b;q=1.0") == [
        ("b", 1.0),
        ("a", 0.5),
    ]


def test_ties_keep_original_order():
    # Stable sort: equal qualities must preserve left-to-right order.
    assert parse_accept_language("fr,de,en") == [
        ("fr", 1.0),
        ("de", 1.0),
        ("en", 1.0),
    ]
    assert parse_accept_language("z;q=0.5,a;q=0.5,m;q=0.5") == [
        ("z", 0.5),
        ("a", 0.5),
        ("m", 0.5),
    ]


def test_q_zero_dropped():
    assert parse_accept_language("en,de;q=0") == [("en", 1.0)]


def test_wildcard_kept():
    assert parse_accept_language("en;q=0.8,*;q=0.1") == [
        ("en", 0.8),
        ("*", 0.1),
    ]


def test_tags_lowercased():
    assert parse_accept_language("EN-GB;Q=0.7") == [("en-gb", 0.7)]


def test_whitespace_trimmed():
    assert parse_accept_language("  en-US , en ; q=0.9 ") == [
        ("en-us", 1.0),
        ("en", 0.9),
    ]


def test_empty_and_trailing_commas_skipped():
    assert parse_accept_language("en,,fr,") == [("en", 1.0), ("fr", 1.0)]


def test_empty_header_returns_empty_list():
    assert parse_accept_language("") == []
    assert parse_accept_language("   ") == []


def test_q_boundary_values():
    assert parse_accept_language("a;q=1,b;q=0.001") == [
        ("a", 1.0),
        ("b", 0.001),
    ]


def test_q_out_of_range_rejected():
    with pytest.raises(ValueError):
        parse_accept_language("en;q=1.5")


def test_q_too_many_decimals_rejected():
    with pytest.raises(ValueError):
        parse_accept_language("en;q=0.1234")


def test_non_numeric_q_rejected():
    with pytest.raises(ValueError):
        parse_accept_language("en;q=high")


def test_unknown_parameter_rejected():
    with pytest.raises(ValueError):
        parse_accept_language("en;level=1")


def test_empty_tag_rejected():
    with pytest.raises(ValueError):
        parse_accept_language(";q=0.5")


def test_return_type():
    result = parse_accept_language("en")
    assert type(result) is list
    assert type(result[0]) is tuple
    assert type(result[0][1]) is float


def test_worked_example():
    assert parse_accept_language("en-US,en;q=0.9,fr;q=0.8,de;q=0") == [
        ("en-us", 1.0),
        ("en", 0.9),
        ("fr", 0.8),
    ]
