import pytest
import yaml

from src.solution import yaml_to_json


def test_rejects_unsafe_yaml(tmp_path):
    p = tmp_path / "evil.yaml"
    p.write_text('!!python/object/apply:os.system ["echo hi"]\n', encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        yaml_to_json(str(p))


def test_empty_file_is_null(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("", encoding="utf-8")
    assert yaml_to_json(str(p)) == "null"
