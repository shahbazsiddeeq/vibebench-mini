import hashlib
import os

import pytest

from src.solution import checksum_manifest

EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
HELLO_SHA = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_empty_dir(tmp_path):
    assert checksum_manifest(str(tmp_path)) == {}


def test_nested_file_uses_posix_key(tmp_path):
    (tmp_path / "x").write_bytes(b"")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "a.txt").write_bytes(b"hello")
    result = checksum_manifest(str(tmp_path))
    assert result == {"x": EMPTY_SHA, "sub/a.txt": HELLO_SHA}


def test_matches_hashlib_for_binary(tmp_path):
    payload = bytes(range(256)) * 500  # 128000 bytes, spans multiple chunks
    (tmp_path / "blob.bin").write_bytes(payload)
    result = checksum_manifest(str(tmp_path))
    assert result == {"blob.bin": hashlib.sha256(payload).hexdigest()}


def test_content_change_changes_digest(tmp_path):
    f = tmp_path / "f.txt"
    f.write_bytes(b"hello")
    before = checksum_manifest(str(tmp_path))["f.txt"]
    f.write_bytes(b"hello!")
    after = checksum_manifest(str(tmp_path))["f.txt"]
    assert before == HELLO_SHA
    assert after != before


def test_root_is_file_raises(tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"x")
    with pytest.raises(NotADirectoryError):
        checksum_manifest(str(f))
