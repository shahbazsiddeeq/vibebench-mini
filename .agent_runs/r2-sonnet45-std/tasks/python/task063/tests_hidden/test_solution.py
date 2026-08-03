import pytest
from src.solution import sha256_file

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_empty_file(tmp_path):
    f = tmp_path / "empty.bin"
    f.write_bytes(b"")
    assert sha256_file(str(f)) == EMPTY_SHA256


def test_consistent(tmp_path):
    f = tmp_path / "f.bin"
    f.write_bytes(b"test")
    assert sha256_file(str(f)) == sha256_file(str(f))


def test_large_file_multiple_chunks(tmp_path):
    # 100000 bytes > the 65536-byte read chunk, so a solution that reads only
    # the first chunk and ignores the rest produces the wrong digest.
    f = tmp_path / "big.bin"
    f.write_bytes(b"a" * 100000)
    assert sha256_file(str(f)) == (
        "6d1cf22d7cc09b085dfc25ee1a1f3ae0265804c607bc2074ad253bcc82fd81ee"
    )
