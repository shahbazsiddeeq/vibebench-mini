import pytest
from src.solution import diff_records


def test_added():
    result = diff_records([], [{"id": 1}], "id")
    assert result["added"] == [{"id": 1}]


def test_no_change():
    r = [{"id": 1, "v": 1}]
    result = diff_records(r, r, "id")
    assert result == {"added": [], "removed": [], "changed": []}


def test_missing_key_from_new_raises():
    with pytest.raises(KeyError):
        diff_records([{"id": 1}], [{"x": 2}], "id")
