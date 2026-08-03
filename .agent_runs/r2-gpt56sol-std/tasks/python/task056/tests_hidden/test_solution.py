import pytest
from src.solution import parse_config


def test_basic(tmp_path):
    f = tmp_path / "app.ini"
    f.write_text("[db]\nhost=localhost\nport=5432\n")
    result = parse_config(str(f))
    assert result == {"db": {"host": "localhost", "port": "5432"}}


def test_blank_lines_ignored(tmp_path):
    f = tmp_path / "app.ini"
    f.write_text("[s1]\nk=v\n\n[s2]\nk2=v2\n")
    result = parse_config(str(f))
    assert "s1" in result and "s2" in result


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_config("/no/such/file.ini")
