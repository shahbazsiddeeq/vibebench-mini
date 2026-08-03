import pytest
from src.solution import tail


def test_basic(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\nc\nd\ne\n")
    assert tail(str(f), 3) == ["c", "d", "e"]


def test_n_zero(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\n")
    assert tail(str(f), 0) == []


def test_n_larger_than_file(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\n")
    assert tail(str(f), 10) == ["a", "b"]


def test_last_line_no_newline(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\nc")
    assert tail(str(f), 2) == ["b", "c"]


def test_n_negative_raises(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\n")
    with pytest.raises(ValueError):
        tail(str(f), -1)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        tail("/no/such/file.txt", 5)
