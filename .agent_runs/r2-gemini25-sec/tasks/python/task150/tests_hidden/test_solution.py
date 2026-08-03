import os

import pytest

from src.solution import rotate_log


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def test_first_write_creates_file(tmp_path):
    log = str(tmp_path / "app.log")
    rotate_log(log, "hello", 10, 2)
    assert read_bytes(log) == b"hello\n"
    assert not os.path.exists(log + ".1")


def test_no_rotation_when_fits(tmp_path):
    log = str(tmp_path / "app.log")
    rotate_log(log, "ab", 100, 2)
    rotate_log(log, "cd", 100, 2)
    assert read_bytes(log) == b"ab\ncd\n"
    assert not os.path.exists(log + ".1")


def test_backups_shift_and_oldest_dropped(tmp_path):
    log = str(tmp_path / "app.log")
    # max_bytes small so every new line forces a rotation.
    rotate_log(log, "one", 5, 2)     # app.log = one
    rotate_log(log, "two", 5, 2)     # one -> .1 ; app.log = two
    rotate_log(log, "three", 5, 2)   # one -> .2 ; two -> .1 ; app.log = three
    rotate_log(log, "four", 5, 2)    # .2(one) dropped ; two -> .2 ; three -> .1 ; app.log = four
    assert read_bytes(log) == b"four\n"
    assert read_bytes(log + ".1") == b"three\n"
    assert read_bytes(log + ".2") == b"two\n"
    assert not os.path.exists(log + ".3")


def test_utf8_byte_length_used(tmp_path):
    log = str(tmp_path / "app.log")
    # 'é' is 2 bytes in UTF-8; line 'é' -> 3 bytes.
    rotate_log(log, "é", 4, 1)       # empty file -> written
    assert read_bytes(log) == "é\n".encode("utf-8")
    rotate_log(log, "é", 4, 1)       # 3+3=6 > 4 -> rotate
    assert read_bytes(log + ".1") == "é\n".encode("utf-8")


def test_invalid_backup_count_raises(tmp_path):
    log = str(tmp_path / "app.log")
    with pytest.raises(ValueError):
        rotate_log(log, "x", 10, -1)
