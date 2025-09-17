from src.solution import column_mean


def test_simple(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("name,score\nA,10\nB,20\nC,30\n", encoding="utf-8")
    assert column_mean(str(p), "score") == 20.0


def test_ignores_bad_rows(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("name,score\nA,10\nB,xx\nC,40\n", encoding="utf-8")
    assert column_mean(str(p), "score") == 25.0


def test_empty_raises(tmp_path):
    p = tmp_path / "e.csv"
    p.write_text("name,score\n", encoding="utf-8")
    import pytest

    with pytest.raises(ValueError):
        column_mean(str(p), "score")
