import pytest
import yaml

from src.solution import yaml_to_json


def test_object_and_list(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text("name: Ada\nnums: [3, 1, 2]\n", encoding="utf-8")
    out = yaml_to_json(str(p))
    # keys sorted: name before nums
    assert out == '{"name":"Ada","nums":[3,1,2]}'


def test_date_serialized_as_string(tmp_path):
    p = tmp_path / "d.yaml"
    p.write_text("d: 2020-01-01\n", encoding="utf-8")
    out = yaml_to_json(str(p))
    assert out == '{"d":"2020-01-01"}'


def test_non_ascii_preserved(tmp_path):
    p = tmp_path / "u.yaml"
    p.write_text("name: café\n", encoding="utf-8")
    assert yaml_to_json(str(p)) == '{"name":"café"}'
