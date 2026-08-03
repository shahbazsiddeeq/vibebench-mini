import pytest
from src.solution import sum_jsonl


def test_empty_raises(tmp_path):
    p = tmp_path / "e.jsonl"
    p.write_text('{"x":"na"}\n{"y":9}\n', encoding="utf-8")
    with pytest.raises(ValueError):
        sum_jsonl(str(p), "x")


def test_floats_and_negatives(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text('{"x":1.5}\n{"x":-2.5}\n{"x":4}\n', encoding="utf-8")
    assert sum_jsonl(str(p), "x") == pytest.approx(3.0)
