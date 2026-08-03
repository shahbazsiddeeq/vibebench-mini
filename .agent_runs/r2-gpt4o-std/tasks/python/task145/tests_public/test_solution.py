import pytest

from src.solution import render_template


def test_basic_substitution():
    assert render_template("{a}-{b}", {"a": "x", "b": "y"}) == "x-y"


def test_empty_template():
    assert render_template("", {"a": 1}) == ""


def test_escaped_braces_only():
    assert render_template("{{}}", {}) == "{}"


def test_underscore_and_digits_in_name():
    assert render_template("{user_1}", {"user_1": "ok"}) == "ok"


def test_missing_key_raises_keyerror():
    with pytest.raises(KeyError):
        render_template("{missing}", {"a": 1})


def test_empty_placeholder_raises_valueerror():
    with pytest.raises(ValueError):
        render_template("{}", {})


def test_illegal_char_in_name_raises():
    with pytest.raises(ValueError):
        render_template("{a b}", {"a b": "x"})


def test_lone_close_brace_raises():
    with pytest.raises(ValueError):
        render_template("a } b", {})


def test_mutation_killer_double_close_not_a_placeholder_terminator():
    # A naive replace-based solution may mishandle the interplay of {{ }} and {name}.
    assert render_template("{{{a}}}", {"a": "V"}) == "{V}"
