import pytest
from src.solution import build_cmd


def test_ok():
    cmd = build_cmd(["tool"], {"verbose": True, "timeout": 5, "output": "out.txt"})
    assert cmd == ["tool", "--verbose", "--timeout", "5", "--output", "out.txt"]


def test_base_as_list_with_leading_args():
    cmd = build_cmd(["python", "-m", "tool"], {"verbose": True})
    assert cmd == ["python", "-m", "tool", "--verbose"]


def test_unknown_key():
    with pytest.raises(ValueError):
        build_cmd("t", {"bad": 1})


def test_bool_not_accepted_as_timeout():
    with pytest.raises(ValueError):
        build_cmd("t", {"timeout": True})
    with pytest.raises(ValueError):
        build_cmd("t", {"timeout": False})


def test_output_nul_byte_rejected():
    with pytest.raises(ValueError):
        build_cmd("t", {"output": "a\x00b"})
