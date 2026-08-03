import os

import pytest

from src.solution import rotate_log


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def test_rotation_when_would_exceed(tmp_path):
    log = str(tmp_path / "app.log")
    rotate_log(log, "hello", 10, 2)
    rotate_log(log, "world", 10, 2)
    assert read_bytes(log) == b"world\n"
    assert read_bytes(log + ".1") == b"hello\n"
    assert not os.path.exists(log + ".2")


def test_oversized_line_on_empty_file_is_written(tmp_path):
    log = str(tmp_path / "app.log")
    rotate_log(log, "x" * 50, 5, 2)
    assert read_bytes(log) == b"x" * 50 + b"\n"
    assert not os.path.exists(log + ".1")


def test_backup_count_zero_discards(tmp_path):
    log = str(tmp_path / "app.log")
    rotate_log(log, "hello", 6, 0)   # 5+1=6 not > 6, fits -> app.log = hello
    rotate_log(log, "world", 6, 0)   # 6+6=12 > 6 -> discard, app.log = world
    assert read_bytes(log) == b"world\n"
    assert not os.path.exists(log + ".1")


def test_invalid_max_bytes_raises(tmp_path):
    log = str(tmp_path / "app.log")
    with pytest.raises(ValueError):
        rotate_log(log, "x", 0, 1)
