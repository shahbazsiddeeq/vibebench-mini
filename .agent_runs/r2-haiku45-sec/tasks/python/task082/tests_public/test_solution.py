import pytest
from src.solution import write_config


def test_empty_config(tmp_path):
    p = tmp_path / "out.ini"
    write_config(str(p), {})
    assert p.exists()


def test_carriage_return_in_value_raises(tmp_path):
    p = tmp_path / "out.ini"
    with pytest.raises(ValueError):
        write_config(str(p), {"s": {"k": "v\ralue"}})


def test_multiple_sections(tmp_path):
    p = tmp_path / "out.ini"
    write_config(str(p), {"a": {"x": "1"}, "b": {"y": "2"}})
    content = p.read_text()
    assert "[a]" in content and "[b]" in content
