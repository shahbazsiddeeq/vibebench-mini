import pytest
from src.solution import build_cmd


def test_base_as_string():
    cmd = build_cmd("tool", {"timeout": 3})
    assert cmd == ["tool", "--timeout", "3"]


def test_verbose_false_appends_nothing():
    assert build_cmd("t", {"verbose": False}) == ["t"]


def test_invalid_values():
    with pytest.raises(ValueError):
        build_cmd("t", {"timeout": 0})
    with pytest.raises(ValueError):
        build_cmd("t", {"output": "bad\nname"})


def test_int_not_accepted_as_verbose():
    with pytest.raises(ValueError):
        build_cmd("t", {"verbose": 1})
