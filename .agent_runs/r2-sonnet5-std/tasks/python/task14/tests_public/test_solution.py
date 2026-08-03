import csv

import pytest
from src.solution import dedupe_csv


def test_missing_key_raises(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    src.write_text("a,b\nx,y\n", encoding="utf-8")
    with pytest.raises(KeyError):
        dedupe_csv(str(src), str(dst), "id")


def test_quoted_fields_preserved(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    src.write_text('id,val\n1,"a,b"\n1,"c, d"\n', encoding="utf-8")
    n = dedupe_csv(str(src), str(dst), "id")
    assert n == 1
    rows = list(csv.DictReader(dst.open(encoding="utf-8")))
    assert rows == [{"id": "1", "val": "c, d"}]
