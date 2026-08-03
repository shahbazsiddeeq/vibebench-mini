from src.solution import TextBuffer

import pytest


def test_append_and_text():
    b = TextBuffer()
    b.append("a")
    b.append("b")
    assert b.text == "ab"


def test_undo_empty_returns_false():
    b = TextBuffer()
    assert b.undo() is False
    assert b.text == ""


def test_new_append_clears_redo_stack():
    b = TextBuffer()
    b.append("a")
    b.append("b")
    b.undo()
    b.append("c")
    assert b.text == "ac"
    assert b.redo() is False


def test_invalid_append_raises():
    b = TextBuffer()
    with pytest.raises(ValueError):
        b.append(123)


def test_multiple_undo_then_multiple_redo_in_order():
    b = TextBuffer()
    for ch in "abc":
        b.append(ch)
    assert b.undo() is True
    assert b.undo() is True
    assert b.text == "a"
    assert b.redo() is True
    assert b.text == "ab"
    assert b.redo() is True
    assert b.text == "abc"
    assert b.redo() is False
