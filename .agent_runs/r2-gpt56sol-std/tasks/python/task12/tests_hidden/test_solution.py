import pytest
from src.solution import dir_hash

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def _make_tree(root, files):
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)


def test_empty_dir_is_empty_digest(tmp_path):
    assert dir_hash(str(tmp_path)) == EMPTY_SHA256


def test_deterministic_across_calls(tmp_path):
    _make_tree(tmp_path, {"x/y.txt": b"data", "z.txt": b"more"})
    assert dir_hash(str(tmp_path)) == dir_hash(str(tmp_path))


def test_rename_changes_hash(tmp_path):
    _make_tree(tmp_path, {"a.txt": b"hi"})
    h1 = dir_hash(str(tmp_path))
    (tmp_path / "a.txt").rename(tmp_path / "b.txt")
    assert dir_hash(str(tmp_path)) != h1


def test_framing_collision_resistance(tmp_path):
    # Two trees that a bare-newline join could confuse must differ.
    d1 = tmp_path / "one"
    d2 = tmp_path / "two"
    _make_tree(d1, {"a": b"b\n1\nc"})
    _make_tree(d2, {"a": b"b", "c": b"1"})
    assert dir_hash(str(d1)) != dir_hash(str(d2))


def test_missing_path_raises(tmp_path):
    with pytest.raises(ValueError):
        dir_hash(str(tmp_path / "does_not_exist"))
