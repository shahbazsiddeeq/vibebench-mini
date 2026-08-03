import pytest

from src.solution import parse_query_string


def test_repeated_keys_accumulate_in_order():
    # Mutation killer: a naive dict-comprehension parser keeps only the
    # last value ({'a': '2'}) instead of collecting a list in order.
    assert parse_query_string("a=1&a=2&a=3") == {"a": ["1", "2", "3"]}


def test_key_without_equals():
    assert parse_query_string("flag") == {"flag": [""]}
    assert parse_query_string("a=1&flag&b=2") == {
        "a": ["1"],
        "flag": [""],
        "b": ["2"],
    }


def test_empty_segments_skipped():
    assert parse_query_string("&&a=1&&&b=2&") == {"a": ["1"], "b": ["2"]}


def test_plus_decoded_to_space():
    assert parse_query_string("q=a+b") == {"q": ["a b"]}


def test_keys_case_sensitive():
    assert parse_query_string("A=1&a=2") == {"A": ["1"], "a": ["2"]}


def test_return_type_is_dict_of_lists():
    result = parse_query_string("a=1")
    assert type(result) is dict
    assert type(result["a"]) is list
