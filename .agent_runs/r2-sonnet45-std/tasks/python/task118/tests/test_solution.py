import pytest
from src.solution import flatten_dict


def test_basic():
    assert flatten_dict({"a": {"b": 1}, "c": 2}) == {"a.b": 1, "c": 2}


def test_deeply_nested():
    assert flatten_dict({"a": {"b": {"c": 1}}}) == {"a.b.c": 1}


def test_flat():
    assert flatten_dict({"x": 1, "y": 2}) == {"x": 1, "y": 2}


def test_custom_sep():
    assert flatten_dict({"a": {"b": 1}}, sep="/") == {"a/b": 1}


def test_empty():
    assert flatten_dict({}) == {}


def test_mixed():
    result = flatten_dict({"a": {"b": 1, "c": {"d": 2}}, "e": 3})
    assert result == {"a.b": 1, "a.c.d": 2, "e": 3}


def test_empty_nested_dict_preserved_as_leaf():
    assert flatten_dict({"a": {}, "b": 1}) == {"a": {}, "b": 1}


def test_nested_empty_dict_keeps_full_path():
    assert flatten_dict({"a": {"b": {}}}) == {"a.b": {}}


def test_separator_collision_raises():
    with pytest.raises(ValueError):
        flatten_dict({"a": {"b": 1}, "a.b": 2})
