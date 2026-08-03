from src.solution import deep_merge


def test_override_takes_precedence():
    result = deep_merge({"a": 1}, {"a": 2})
    assert result == {"a": 2}


def test_does_not_mutate_override():
    override = {"a": {"y": 2}}
    deep_merge({"a": {"x": 1}}, override)
    assert override == {"a": {"y": 2}}


def test_non_dict_override_replaces():
    result = deep_merge({"a": {"x": 1}}, {"a": "flat"})
    assert result == {"a": "flat"}


def test_scalar_conflict_takes_override():
    result = deep_merge({"a": 1, "b": 2}, {"b": 99})
    assert result == {"a": 1, "b": 99}
