import pytest
from src.solution import diff_records


def test_basic_change():
    old = [{"id": 1, "v": 1}]
    new = [{"id": 1, "v": 2}]
    result = diff_records(old, new, "id")
    assert result["changed"] == [{"id": 1, "v": 2}]
    assert result["added"] == []
    assert result["removed"] == []


def test_added():
    result = diff_records([], [{"id": 1}], "id")
    assert result["added"] == [{"id": 1}]


def test_removed():
    result = diff_records([{"id": 1}], [], "id")
    assert result["removed"] == [{"id": 1}]


def test_no_change():
    r = [{"id": 1, "v": 1}]
    result = diff_records(r, r, "id")
    assert result == {"added": [], "removed": [], "changed": []}


def test_missing_key_raises():
    with pytest.raises(KeyError):
        diff_records([{"x": 1}], [], "id")


def test_missing_key_from_new_raises():
    with pytest.raises(KeyError):
        diff_records([{"id": 1}], [{"x": 2}], "id")


def test_mixed_multi_record():
    old = [{"id": 1, "v": 1}, {"id": 2, "v": 2}, {"id": 3, "v": 3}]
    new = [{"id": 1, "v": 1}, {"id": 2, "v": 99}, {"id": 4, "v": 4}]
    result = diff_records(old, new, "id")
    assert result["added"] == [{"id": 4, "v": 4}]
    assert result["removed"] == [{"id": 3, "v": 3}]
    assert result["changed"] == [{"id": 2, "v": 99}]
