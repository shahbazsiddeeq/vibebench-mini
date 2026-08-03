import pytest
from src.solution import count_lines


def test_basic(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("line1\nline2\nline3\n")
    assert count_lines(str(f)) == 3


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    assert count_lines(str(f)) == 0


def test_single_line_no_newline(tmp_path):
    f = tmp_path / "one.txt"
    f.write_text("hello")
    assert count_lines(str(f)) == 1


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        count_lines("/nonexistent/file.txt")


def test_multiple_lines(tmp_path):
    f = tmp_path / "multi.txt"
    f.write_text("\n".join(str(i) for i in range(10)) + "\n")
    assert count_lines(str(f)) == 10
