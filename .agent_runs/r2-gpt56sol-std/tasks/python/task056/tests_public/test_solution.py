import pytest
from src.solution import parse_config


def test_comments_ignored(tmp_path):
    f = tmp_path / "app.ini"
    f.write_text("[section]\n# comment\nkey=value\n")
    result = parse_config(str(f))
    assert result == {"section": {"key": "value"}}


def test_duplicate_section_raises(tmp_path):
    f = tmp_path / "app.ini"
    f.write_text("[s]\nk=v\n[s]\nk=v\n")
    with pytest.raises(ValueError):
        parse_config(str(f))


def test_multiple_sections(tmp_path):
    f = tmp_path / "app.ini"
    f.write_text("[a]\nx=1\n[b]\ny=2\n")
    result = parse_config(str(f))
    assert result["a"]["x"] == "1"
    assert result["b"]["y"] == "2"
