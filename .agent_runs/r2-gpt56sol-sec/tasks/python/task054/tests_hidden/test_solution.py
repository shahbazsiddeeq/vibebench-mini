import os

from src.solution import find_by_ext


def test_finds_files(tmp_path):
    (tmp_path / "a.py").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    result = find_by_ext(str(tmp_path), ".py")
    assert len(result) == 1
    assert result[0].endswith("a.py")


def test_recursive(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.py").write_text("")
    (sub / "b.py").write_text("")
    result = find_by_ext(str(tmp_path), ".py")
    assert len(result) == 2


def test_sorted(tmp_path):
    for name in ["z.py", "a.py", "m.py"]:
        (tmp_path / name).write_text("")
    result = find_by_ext(str(tmp_path), ".py")
    assert result == sorted(result)
