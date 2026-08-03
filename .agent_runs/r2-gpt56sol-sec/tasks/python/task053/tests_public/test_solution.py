import pytest
from src.solution import count_lines


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    assert count_lines(str(f)) == 0


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        count_lines("/nonexistent/file.txt")
