import hashlib
import os

import pytest

from src.solution import checksum_manifest

EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
HELLO_SHA = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_single_empty_file(tmp_path):
    (tmp_path / "x").write_bytes(b"")
    assert checksum_manifest(str(tmp_path)) == {"x": EMPTY_SHA}


def test_keys_sorted_ascending(tmp_path):
    for name in ["c.txt", "a.txt", "b.txt"]:
        (tmp_path / name).write_bytes(b"data")
    keys = list(checksum_manifest(str(tmp_path)).keys())
    assert keys == ["a.txt", "b.txt", "c.txt"]


def test_deep_nesting(tmp_path):
    deep = tmp_path / "a" / "b" / "c"
    deep.mkdir(parents=True)
    (deep / "f.txt").write_bytes(b"hello")
    result = checksum_manifest(str(tmp_path))
    assert result == {"a/b/c/f.txt": HELLO_SHA}


def test_missing_root_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        checksum_manifest(str(tmp_path / "nope"))
