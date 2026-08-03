import pytest
from src.solution import flatten_dict


def test_deeply_nested():
    assert flatten_dict({"a": {"b": {"c": 1}}}) == {"a.b.c": 1}


def test_custom_sep():
    assert flatten_dict({"a": {"b": 1}}, sep="/") == {"a/b": 1}


def test_mixed():
    result = flatten_dict({"a": {"b": 1, "c": {"d": 2}}, "e": 3})
    assert result == {"a.b": 1, "a.c.d": 2, "e": 3}


def test_nested_empty_dict_keeps_full_path():
    assert flatten_dict({"a": {"b": {}}}) == {"a.b": {}}
