import pytest

from src.solution import Editor, Memento


def test_worked_example_restore():
    e = Editor()
    e.write("ab")
    m = e.save()
    e.write("cd")
    assert e.content == "abcd"
    e.restore(m)
    assert e.content == "ab"


def test_starts_empty():
    assert Editor().content == ""


def test_clear():
    e = Editor()
    e.write("data")
    e.clear()
    assert e.content == ""


def test_multiple_undo_lifo():
    e = Editor()
    e.write("a")
    e.save()
    e.write("b")
    e.save()
    e.write("c")
    assert e.undo() == "ab"
    assert e.undo() == "a"


def test_memento_state_is_read_only():
    m = Editor().save()
    with pytest.raises(AttributeError):
        m.state = "hacked"


def test_restore_type_error():
    with pytest.raises(TypeError):
        Editor().restore("not a memento")
