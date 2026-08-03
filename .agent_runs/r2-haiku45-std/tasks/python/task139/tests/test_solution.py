from src.solution import expand_cases
import pytest


def test_basic():
    result = expand_cases({"a": 1, "b": 2}, [{"b": 9}, {"a": 7}])
    assert result == [{"a": 1, "b": 9}, {"a": 7, "b": 2}]


def test_empty_overrides():
    assert expand_cases({"a": 1}, []) == []


def test_base_not_mutated():
    base = {"a": 1, "b": 2}
    expand_cases(base, [{"a": 99}])
    assert base == {"a": 1, "b": 2}


def test_results_are_new_dicts():
    base = {"a": 1}
    result = expand_cases(base, [{"b": 2}])
    assert result[0] is not base
    result[0]["a"] = 100
    assert base == {"a": 1}


def test_override_adds_new_keys():
    result = expand_cases({"a": 1}, [{"c": 3}])
    assert result == [{"a": 1, "c": 3}]


def test_empty_override_dict_copies_base():
    base = {"a": 1, "b": 2}
    result = expand_cases(base, [{}])
    assert result == [{"a": 1, "b": 2}]
    # An empty override must produce a copy, not an alias of base.
    assert result[0] is not base


def test_merge_is_shallow_not_deep():
    # A nested dict in the override replaces the base's nested dict entirely;
    # a deep merge would instead yield {"cfg": {"x": 1, "y": 2}}.
    result = expand_cases({"cfg": {"x": 1}, "n": 0}, [{"cfg": {"y": 2}}])
    assert result == [{"cfg": {"y": 2}, "n": 0}]


def test_shallow_copy_shares_untouched_nested_value():
    # For keys the override does not touch, the shallow copy references the same
    # nested object as base (this pins shallow-copy semantics).
    base = {"cfg": {"x": 1}}
    result = expand_cases(base, [{"other": 5}])
    assert result[0] == {"cfg": {"x": 1}, "other": 5}
    assert result[0]["cfg"] is base["cfg"]


def test_multiple_overrides_independent():
    result = expand_cases({"x": 0}, [{"x": 1}, {"x": 2}, {"x": 3}])
    assert result == [{"x": 1}, {"x": 2}, {"x": 3}]
