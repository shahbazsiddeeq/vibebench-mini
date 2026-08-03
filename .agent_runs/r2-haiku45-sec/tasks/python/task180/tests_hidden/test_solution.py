import pytest

from src.solution import File, Directory


def test_file_total_size():
    assert File("a.txt", 10).total_size() == 10
    assert File("empty", 0).total_size() == 0


def test_add_returns_self_for_chaining():
    d = Directory("d")
    assert d.add(File("x", 1)) is d


def test_directories_not_counted_as_files():
    root = Directory("root")
    root.add(Directory("empty1")).add(Directory("empty2"))
    assert root.count_files() == 0
    assert root.total_size() == 0
    assert root.list_paths() == []


def test_invalid_file_size():
    with pytest.raises(ValueError):
        File("a", -1)
    with pytest.raises(ValueError):
        File("a", 1.5)
    with pytest.raises(ValueError):
        File("a", True)


def test_add_wrong_type_raises_typeerror():
    with pytest.raises(TypeError):
        Directory("d").add("not a node")
    with pytest.raises(TypeError):
        Directory("d").add(42)
