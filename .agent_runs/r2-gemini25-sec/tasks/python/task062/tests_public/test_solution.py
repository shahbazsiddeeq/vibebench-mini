import hashlib

from src.solution import find_duplicates


def test_key_is_sha256_digest(tmp_path):
    content = b"hello world"
    (tmp_path / "a.txt").write_bytes(content)
    (tmp_path / "b.txt").write_bytes(content)
    result = find_duplicates(str(tmp_path))
    key = list(result.keys())[0]
    # Must be a 64-char lowercase hex SHA-256 digest, not MD5 (32) or anything else.
    assert len(key) == 64
    assert all(c in "0123456789abcdef" for c in key)
    assert key == hashlib.sha256(content).hexdigest()


def test_zero_byte_files_are_grouped(tmp_path):
    (tmp_path / "e1.txt").write_bytes(b"")
    (tmp_path / "e2.txt").write_bytes(b"")
    result = find_duplicates(str(tmp_path))
    assert len(result) == 1
    key = list(result.keys())[0]
    assert key == hashlib.sha256(b"").hexdigest()
    assert len(list(result.values())[0]) == 2


def test_empty_dir(tmp_path):
    assert find_duplicates(str(tmp_path)) == {}


def test_mixed(tmp_path):
    (tmp_path / "x.txt").write_bytes(b"unique")
    (tmp_path / "y.txt").write_bytes(b"dup")
    (tmp_path / "z.txt").write_bytes(b"dup")
    result = find_duplicates(str(tmp_path))
    assert len(result) == 1
