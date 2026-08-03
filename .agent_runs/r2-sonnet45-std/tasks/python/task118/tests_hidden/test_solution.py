import pytest
from src.solution import flatten_dict


def test_basic():
    assert flatten_dict({"a": {"b": 1}, "c": 2}) == {"a.b": 1, "c": 2}


def test_flat():
    assert flatten_dict({"x": 1, "y": 2}) == {"x": 1, "y": 2}


def test_empty():
    assert flatten_dict({}) == {}


def test_empty_nested_dict_preserved_as_leaf():
    assert flatten_dict({"a": {}, "b": 1}) == {"a": {}, "b": 1}


def test_separator_collision_raises():
    with pytest.raises(ValueError):
        flatten_dict({"a": {"b": 1}, "a.b": 2})
