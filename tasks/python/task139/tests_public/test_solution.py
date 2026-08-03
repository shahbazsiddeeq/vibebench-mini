from src.solution import expand_cases
import pytest


def test_empty_overrides():
    assert expand_cases({"a": 1}, []) == []


def test_results_are_new_dicts():
    base = {"a": 1}
    result = expand_cases(base, [{"b": 2}])
    assert result[0] is not base
    result[0]["a"] = 100
    assert base == {"a": 1}


def test_empty_override_dict_copies_base():
    base = {"a": 1, "b": 2}
    result = expand_cases(base, [{}])
    assert result == [{"a": 1, "b": 2}]
    # An empty override must produce a copy, not an alias of base.
    assert result[0] is not base


def test_shallow_copy_shares_untouched_nested_value():
    # For keys the override does not touch, the shallow copy references the same
    # nested object as base (this pins shallow-copy semantics).
    base = {"cfg": {"x": 1}}
    result = expand_cases(base, [{"other": 5}])
    assert result[0] == {"cfg": {"x": 1}, "other": 5}
    assert result[0]["cfg"] is base["cfg"]
