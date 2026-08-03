import json

import pytest
from src.solution import merge_json_files


def test_later_overrides(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    out = tmp_path / "out.json"
    a.write_text('{"k": 1}')
    b.write_text('{"k": 2}')
    merge_json_files([str(a), str(b)], str(out))
    assert json.loads(out.read_text())["k"] == 2


def test_shallow_merge_replaces_nested_object(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    out = tmp_path / "out.json"
    a.write_text('{"cfg": {"x": 1, "y": 2}, "keep": 9}')
    b.write_text('{"cfg": {"y": 3}}')
    merge_json_files([str(a), str(b)], str(out))
    result = json.loads(out.read_text())
    # shallow: the whole "cfg" object is replaced, "x" is dropped
    assert result == {"cfg": {"y": 3}, "keep": 9}


def test_empty_list(tmp_path):
    out = tmp_path / "out.json"
    merge_json_files([], str(out))
    assert json.loads(out.read_text()) == {}
