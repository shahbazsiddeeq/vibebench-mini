import pytest
from src.solution import dir_size


def test_basic(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world!")
    assert dir_size(str(tmp_path)) == 11


def test_empty_dir(tmp_path):
    assert dir_size(str(tmp_path)) == 0


def test_nested(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.txt").write_bytes(b"x" * 100)
    (sub / "b.txt").write_bytes(b"y" * 200)
    assert dir_size(str(tmp_path)) == 300


def test_not_a_directory(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hi")
    with pytest.raises(NotADirectoryError):
        dir_size(str(f))


def test_nonexistent_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        dir_size(str(tmp_path / "nope"))


def test_symlinks_not_counted(tmp_path):
    import os

    real = tmp_path / "real.txt"
    real.write_bytes(b"z" * 50)
    # a symlink pointing at the real file must not add to the total
    os.symlink(str(real), str(tmp_path / "link.txt"))
    assert dir_size(str(tmp_path)) == 50
