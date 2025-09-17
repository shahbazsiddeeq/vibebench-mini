import pytest
from src.solution import build_cmd


def test_ok():
    cmd = build_cmd(["tool"], {"verbose": True, "timeout": 5, "output": "out.txt"})
    assert cmd == ["tool", "--verbose", "--timeout", "5", "--output", "out.txt"]


def test_unknown_key():
    with pytest.raises(ValueError):
        build_cmd("t", {"bad": 1})


def test_invalid_values():
    with pytest.raises(ValueError):
        build_cmd("t", {"timeout": 0})
    with pytest.raises(ValueError):
        build_cmd("t", {"output": "bad\nname"})
