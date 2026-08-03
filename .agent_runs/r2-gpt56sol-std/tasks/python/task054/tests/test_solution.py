import os

from src.solution import find_by_ext


def test_finds_files(tmp_path):
    (tmp_path / "a.py").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    result = find_by_ext(str(tmp_path), ".py")
    assert len(result) == 1
    assert result[0].endswith("a.py")


def test_returns_absolute_paths(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "a.py").write_text("")
    # call with a relative root so a relative-path implementation would be caught
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = find_by_ext("sub", ".py")
    finally:
        os.chdir(cwd)
    assert len(result) == 1
    assert os.path.isabs(result[0])
    assert result[0] == str((sub / "a.py").resolve())


def test_recursive(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.py").write_text("")
    (sub / "b.py").write_text("")
    result = find_by_ext(str(tmp_path), ".py")
    assert len(result) == 2


def test_no_match(tmp_path):
    (tmp_path / "a.txt").write_text("")
    assert find_by_ext(str(tmp_path), ".py") == []


def test_sorted(tmp_path):
    for name in ["z.py", "a.py", "m.py"]:
        (tmp_path / name).write_text("")
    result = find_by_ext(str(tmp_path), ".py")
    assert result == sorted(result)


def test_without_dot(tmp_path):
    (tmp_path / "test.py").write_text("")
    result = find_by_ext(str(tmp_path), "py")
    assert len(result) == 1
