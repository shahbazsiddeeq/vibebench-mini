import pytest
from src.solution import sum_jsonl


def test_basic(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text('{"x":1}\n{"x":2}\n{"x":"na"}\n{"y":9}\n', encoding="utf-8")
    assert sum_jsonl(str(p), "x") == 3.0


def test_ignores_blank_and_malformed_lines(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text('{"x":2}\n\n   \nnot json\n{"x":3}\n', encoding="utf-8")
    assert sum_jsonl(str(p), "x") == 5.0


def test_all_malformed_raises(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text("garbage\n{bad}\n\n", encoding="utf-8")
    with pytest.raises(ValueError):
        sum_jsonl(str(p), "x")
