import pytest
from src.solution import write_config


def test_basic(tmp_path):
    p = tmp_path / "out.ini"
    write_config(str(p), {"db": {"host": "localhost", "port": "5432"}})
    content = p.read_text()
    assert "[db]" in content
    assert "host=localhost" in content


def test_newline_in_value_raises(tmp_path):
    p = tmp_path / "out.ini"
    with pytest.raises(ValueError):
        write_config(str(p), {"s": {"k": "v\nalue"}})


def test_exact_format_no_spaces(tmp_path):
    p = tmp_path / "out.ini"
    write_config(str(p), {"db": {"host": "localhost"}})
    assert p.read_text() == "[db]\nhost=localhost\n"
