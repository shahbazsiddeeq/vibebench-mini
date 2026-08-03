import pytest

from src.solution import File, Directory


def test_file_total_size():
    assert File("a.txt", 10).total_size() == 10
    assert File("empty", 0).total_size() == 0


def test_worked_example():
    root = Directory("root")
    root.add(File("a.txt", 10)).add(Directory("sub").add(File("b.txt", 5)))
    assert root.total_size() == 15
    assert root.count_files() == 2
    assert root.list_paths() == ["a.txt", "sub/b.txt"]


def test_add_returns_self_for_chaining():
    d = Directory("d")
    assert d.add(File("x", 1)) is d


def test_nested_recursion():
    root = Directory("root")
    sub = Directory("sub")
    deep = Directory("deep")
    deep.add(File("z.bin", 100))
    sub.add(File("y.bin", 20)).add(deep)
    root.add(File("x.bin", 3)).add(sub)
    assert root.total_size() == 123
    assert root.count_files() == 3
    assert root.list_paths() == ["sub/deep/z.bin", "sub/y.bin", "x.bin"]


def test_directories_not_counted_as_files():
    root = Directory("root")
    root.add(Directory("empty1")).add(Directory("empty2"))
    assert root.count_files() == 0
    assert root.total_size() == 0
    assert root.list_paths() == []


def test_list_paths_sorted():
    root = Directory("root")
    root.add(File("zeta", 1)).add(File("alpha", 1)).add(File("mid", 1))
    assert root.list_paths() == ["alpha", "mid", "zeta"]


def test_invalid_file_size():
    with pytest.raises(ValueError):
        File("a", -1)
    with pytest.raises(ValueError):
        File("a", 1.5)
    with pytest.raises(ValueError):
        File("a", True)


def test_invalid_name():
    with pytest.raises(ValueError):
        File("", 1)
    with pytest.raises(ValueError):
        File("a/b", 1)
    with pytest.raises(ValueError):
        Directory("")


def test_add_wrong_type_raises_typeerror():
    with pytest.raises(TypeError):
        Directory("d").add("not a node")
    with pytest.raises(TypeError):
        Directory("d").add(42)


def test_duplicate_name_raises():
    d = Directory("d")
    d.add(File("dup", 1))
    with pytest.raises(ValueError):
        d.add(File("dup", 2))
    with pytest.raises(ValueError):
        d.add(Directory("dup"))
