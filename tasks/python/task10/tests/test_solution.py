from src.solution import yaml_to_json


def test_object_and_list(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text("name: Ada\nnums: [3, 1, 2]\n", encoding="utf-8")
    out = yaml_to_json(str(p))
    # keys sorted: name before nums
    assert out == '{"name":"Ada","nums":[3,1,2]}'
