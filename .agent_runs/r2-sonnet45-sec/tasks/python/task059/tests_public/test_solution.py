import pytest
from src.solution import tail


def test_n_zero(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\n")
    assert tail(str(f), 0) == []


def test_last_line_no_newline(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text("a\nb\nc")
    assert tail(str(f), 2) == ["b", "c"]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        tail("/no/such/file.txt", 5)
