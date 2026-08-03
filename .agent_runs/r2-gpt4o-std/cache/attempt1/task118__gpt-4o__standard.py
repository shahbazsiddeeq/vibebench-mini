# src/solution.py

def flatten_dict(d, sep="."):
    def _flatten(current, parent_key=""):
        items = {}
        for k, v in current.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict) and v:
                items.update(_flatten(v, new_key))
            else:
                if new_key in items:
                    raise ValueError(f"Collision detected for key: {new_key}")
                items[new_key] = v
        return items

    return _flatten(d)

# Unit tests
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

def test_empty_dict():
    assert flatten_dict({}) == {}

def test_collision():
    with pytest.raises(ValueError):
        flatten_dict({"a": {"b": 1}, "a.b": 2})

def test_single_level():
    assert flatten_dict({"a": 1, "b": 2}) == {"a": 1, "b": 2}

def test_empty_nested_dict():
    assert flatten_dict({"a": {}}) == {"a": {}}
