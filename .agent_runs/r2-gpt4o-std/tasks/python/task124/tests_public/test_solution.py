from src.solution import TextBuffer

import pytest


def test_undo_then_redo():
    b = TextBuffer()
    b.append("a")
    b.append("b")
    assert b.undo() is True
    assert b.text == "a"
    assert b.redo() is True
    assert b.text == "ab"


def test_redo_without_undo_returns_false():
    b = TextBuffer()
    b.append("x")
    assert b.redo() is False


def test_multiple_undo():
    b = TextBuffer()
    b.append("a")
    b.append("b")
    b.append("c")
    b.undo()
    b.undo()
    assert b.text == "a"


def test_invalid_append_does_not_change_text():
    b = TextBuffer()
    b.append("a")
    with pytest.raises(ValueError):
        b.append(123)
    assert b.text == "a"
