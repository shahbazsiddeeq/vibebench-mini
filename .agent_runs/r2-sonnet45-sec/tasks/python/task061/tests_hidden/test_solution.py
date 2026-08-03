import pytest
from src.solution import dir_size


def test_basic(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world!")
    assert dir_size(str(tmp_path)) == 11


def test_nested(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.txt").write_bytes(b"x" * 100)
    (sub / "b.txt").write_bytes(b"y" * 200)
    assert dir_size(str(tmp_path)) == 300


def test_nonexistent_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        dir_size(str(tmp_path / "nope"))
