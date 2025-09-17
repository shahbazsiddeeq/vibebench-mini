from src.solution import sum_jsonl
import pytest

def test_basic(tmp_path):
    p = tmp_path/"d.jsonl"
    p.write_text('{"x":1}\n{"x":2}\n{"x":"na"}\n{"y":9}\n', encoding="utf-8")
    assert sum_jsonl(str(p), "x") == 3.0

def test_empty_raises(tmp_path):
    p = tmp_path/"e.jsonl"
    p.write_text('{"x":"na"}\n{"y":9}\n', encoding="utf-8")
    with pytest.raises(ValueError):
        sum_jsonl(str(p), "x")
