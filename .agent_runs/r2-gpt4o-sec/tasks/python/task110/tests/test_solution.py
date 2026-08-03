from src.solution import deep_merge


def test_basic_merge():
    result = deep_merge({"a": {"x": 1}}, {"a": {"y": 2}})
    assert result == {"a": {"x": 1, "y": 2}}


def test_override_takes_precedence():
    result = deep_merge({"a": 1}, {"a": 2})
    assert result == {"a": 2}


def test_does_not_mutate_base():
    base = {"a": {"x": 1}}
    deep_merge(base, {"a": {"y": 2}})
    assert base == {"a": {"x": 1}}


def test_does_not_mutate_override():
    override = {"a": {"y": 2}}
    deep_merge({"a": {"x": 1}}, override)
    assert override == {"a": {"y": 2}}


def test_nested_override():
    result = deep_merge({"a": {"b": {"c": 1}}}, {"a": {"b": {"d": 2}}})
    assert result == {"a": {"b": {"c": 1, "d": 2}}}


def test_non_dict_override_replaces():
    result = deep_merge({"a": {"x": 1}}, {"a": "flat"})
    assert result == {"a": "flat"}


def test_list_conflict_overrides_not_concatenated():
    result = deep_merge({"a": [1, 2]}, {"a": [3, 4]})
    assert result == {"a": [3, 4]}


def test_scalar_conflict_takes_override():
    result = deep_merge({"a": 1, "b": 2}, {"b": 99})
    assert result == {"a": 1, "b": 99}


def test_untouched_nested_dict_is_shared_with_base():
    base = {"a": {"x": 1}}
    result = deep_merge(base, {"b": 2})
    # 'a' was not overridden, so the merged result shares the same object.
    assert result["a"] is base["a"]
