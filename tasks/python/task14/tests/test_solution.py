import csv

import pytest
from src.solution import dedupe_csv


def test_keep_last(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    src.write_text("id,val\n1,a\n2,b\n1,c\n3,d\n2,z\n", encoding="utf-8")
    n = dedupe_csv(str(src), str(dst), "id")
    assert n == 3
    rows = list(csv.DictReader(dst.open(encoding="utf-8")))
    # last of id=1 is c; last of id=2 is z
    assert rows[0]["id"] == "1" and rows[0]["val"] == "c"
    assert rows[1]["id"] == "3" and rows[1]["val"] == "d"
    assert rows[2]["id"] == "2" and rows[2]["val"] == "z"


def test_missing_key_raises(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    src.write_text("a,b\nx,y\n", encoding="utf-8")
    with pytest.raises(KeyError):
        dedupe_csv(str(src), str(dst), "id")
