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


def test_worked_example_undo():
    e2 = Editor()
    e2.write("x")
    e2.save()
    e2.write("y")
    assert e2.undo() == "x"


def test_starts_empty():
    assert Editor().content == ""


def test_write_appends():
    e = Editor()
    e.write("foo")
    e.write("bar")
    assert e.content == "foobar"


def test_clear():
    e = Editor()
    e.write("data")
    e.clear()
    assert e.content == ""


def test_restore_does_not_mutate_memento_state():
    e = Editor()
    e.write("state1")
    m = e.save()
    e.write("more")
    e.restore(m)
    # Restoring must not corrupt the captured snapshot; restore is repeatable.
    assert m.state == "state1"
    e.write("XYZ")
    e.restore(m)
    assert e.content == "state1"


def test_multiple_undo_lifo():
    e = Editor()
    e.write("a")
    e.save()
    e.write("b")
    e.save()
    e.write("c")
    assert e.undo() == "ab"
    assert e.undo() == "a"


def test_undo_empty_raises():
    with pytest.raises(IndexError):
        Editor().undo()


def test_memento_state_is_read_only():
    m = Editor().save()
    with pytest.raises(AttributeError):
        m.state = "hacked"


def test_write_type_error():
    with pytest.raises(TypeError):
        Editor().write(123)


def test_restore_type_error():
    with pytest.raises(TypeError):
        Editor().restore("not a memento")
