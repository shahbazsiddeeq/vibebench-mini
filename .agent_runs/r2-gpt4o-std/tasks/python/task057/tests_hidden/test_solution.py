import json

import pytest
from src.solution import merge_json_files


def test_basic_merge(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    out = tmp_path / "out.json"
    a.write_text('{"x": 1}')
    b.write_text('{"y": 2}')
    merge_json_files([str(a), str(b)], str(out))
    result = json.loads(out.read_text())
    assert result == {"x": 1, "y": 2}


def test_not_object_raises(tmp_path):
    a = tmp_path / "a.json"
    a.write_text("[1, 2, 3]")
    out = tmp_path / "out.json"
    with pytest.raises(ValueError):
        merge_json_files([str(a)], str(out))


def test_three_file_precedence_chain(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    c = tmp_path / "c.json"
    out = tmp_path / "out.json"
    a.write_text('{"k": 1, "a": "A"}')
    b.write_text('{"k": 2, "b": "B"}')
    c.write_text('{"k": 3, "c": "C"}')
    merge_json_files([str(a), str(b), str(c)], str(out))
    result = json.loads(out.read_text())
    assert result == {"k": 3, "a": "A", "b": "B", "c": "C"}
