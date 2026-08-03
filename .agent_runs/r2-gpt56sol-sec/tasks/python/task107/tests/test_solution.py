import pytest
from src.solution import assert_dict_subset


def test_passes_when_subset():
    assert_dict_subset({"a": 1, "b": 2}, {"a": 1})


def test_passes_with_extra_keys():
    assert_dict_subset({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2})


def test_fails_missing_key():
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({"a": 1}, {"b": 2})
    assert "Missing key" in str(exc.value)


def test_fails_wrong_value():
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({"a": 1}, {"a": 2})
    assert "expected" in str(exc.value)


def test_empty_expected_always_passes():
    assert_dict_subset({}, {})
    assert_dict_subset({"a": 1}, {})


def test_reports_all_mismatches():
    # Two problems at once: 'x' has the wrong value, 'y' is missing entirely.
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({"x": 1}, {"x": 2, "y": 3})
    msg = str(exc.value)
    # The wrong-value mismatch must be reported with 'expected' and both values.
    assert "expected" in msg
    assert "2" in msg and "1" in msg
    # The missing key must also be reported, not swallowed.
    assert "Missing key" in msg
    assert "y" in msg


def test_reports_every_missing_key():
    with pytest.raises(AssertionError) as exc:
        assert_dict_subset({}, {"a": 1, "b": 2})
    msg = str(exc.value)
    assert msg.count("Missing key") == 2
    assert "a" in msg and "b" in msg
