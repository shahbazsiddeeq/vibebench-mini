import pytest
from src.solution import column_mean


def test_ignores_bad_rows(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("name,score\nA,10\nB,xx\nC,40\n", encoding="utf-8")
    assert column_mean(str(p), "score") == 25.0


def test_missing_column_raises(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text("name,score\nA,10\nB,20\n", encoding="utf-8")
    with pytest.raises(ValueError):
        column_mean(str(p), "nope")


def test_all_non_numeric_raises(tmp_path):
    p = tmp_path / "nn.csv"
    p.write_text("name,score\nA,foo\nB,bar\n", encoding="utf-8")
    with pytest.raises(ValueError):
        column_mean(str(p), "score")
