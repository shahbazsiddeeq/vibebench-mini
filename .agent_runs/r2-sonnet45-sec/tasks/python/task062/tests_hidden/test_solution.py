import hashlib

from src.solution import find_duplicates


def test_two_identical_files(tmp_path):
    content = b"hello world"
    (tmp_path / "a.txt").write_bytes(content)
    (tmp_path / "b.txt").write_bytes(content)
    result = find_duplicates(str(tmp_path))
    assert len(result) == 1
    paths = list(result.values())[0]
    assert len(paths) == 2


def test_finds_duplicates_in_subdirectories(tmp_path):
    content = b"nested dup"
    sub = tmp_path / "sub" / "deep"
    sub.mkdir(parents=True)
    (tmp_path / "top.txt").write_bytes(content)
    (sub / "bottom.txt").write_bytes(content)
    result = find_duplicates(str(tmp_path))
    assert len(result) == 1
    paths = list(result.values())[0]
    assert len(paths) == 2
    assert str(tmp_path / "top.txt") in paths
    assert str(sub / "bottom.txt") in paths


def test_no_duplicates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"aaa")
    (tmp_path / "b.txt").write_bytes(b"bbb")
    assert find_duplicates(str(tmp_path)) == {}


def test_three_identical(tmp_path):
    for name in ["a.txt", "b.txt", "c.txt"]:
        (tmp_path / name).write_bytes(b"same")
    result = find_duplicates(str(tmp_path))
    paths = list(result.values())[0]
    assert len(paths) == 3
