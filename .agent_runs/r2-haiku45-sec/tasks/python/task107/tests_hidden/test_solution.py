import pytest
from src.solution import assert_dict_subset


def test_passes_when_subset():
    assert_dict_subset({"a": 1, "b": 2}, {"a": 1})


def test_fails_missing_key():
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({"a": 1}, {"b": 2})
    assert "Missing key" in str(exc.value)


def test_empty_expected_always_passes():
    assert_dict_subset({}, {})
    assert_dict_subset({"a": 1}, {})


def test_reports_every_missing_key():
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({}, {"a": 1, "b": 2})
    msg = str(exc.value)
    assert msg.count("Missing key") == 2
    assert "a" in msg and "b" in msg
