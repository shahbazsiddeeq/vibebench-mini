import pytest
from src.solution import sha256_file

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_known_content(tmp_path):
    f = tmp_path / "data.txt"
    f.write_bytes(b"hello")
    result = sha256_file(str(f))
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        sha256_file("/no/such/file")


def test_returns_hex_string(tmp_path):
    f = tmp_path / "f.bin"
    f.write_bytes(b"data")
    result = sha256_file(str(f))
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)
