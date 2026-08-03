import pytest

from src.solution import parse_query_string


def test_basic_pairs():
    assert parse_query_string("a=1&b=2") == {"a": ["1"], "b": ["2"]}


def test_blank_value():
    assert parse_query_string("a=") == {"a": [""]}


def test_empty_string_returns_empty_dict():
    assert parse_query_string("") == {}


def test_split_on_first_equals_only():
    assert parse_query_string("a=b=c") == {"a": ["b=c"]}


def test_percent_decoding_in_key_and_value():
    assert parse_query_string("x%20y=a%2Bb") == {"x y": ["a+b"]}


def test_value_with_encoded_ampersand():
    assert parse_query_string("q=a%26b") == {"q": ["a&b"]}


def test_worked_example():
    assert parse_query_string("a=1&a=2&b=&c") == {
        "a": ["1", "2"],
        "b": [""],
        "c": [""],
    }
