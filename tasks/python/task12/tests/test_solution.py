from src.solution import dir_hash


def test_changes_on_content_or_name(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    f1 = d / "a.txt"
    f1.write_text("hi", encoding="utf-8")
    f2 = d / "b.txt"
    f2.write_text("there", encoding="utf-8")
    h1 = dir_hash(str(d))

    # change content -> hash changes
    f2.write_text("there!", encoding="utf-8")
    h2 = dir_hash(str(d))
    assert h2 != h1

    # revert and rename file -> hash changes
    f2.write_text("there", encoding="utf-8")
    h3 = dir_hash(str(d))
    (d / "c.txt").write_text(f2.read_text(encoding="utf-8"), encoding="utf-8")
    f2.unlink()
    h4 = dir_hash(str(d))
    assert h4 != h3
