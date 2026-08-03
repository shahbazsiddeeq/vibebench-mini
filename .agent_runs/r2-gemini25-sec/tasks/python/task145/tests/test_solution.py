import pytest

from src.solution import render_template


def test_worked_example():
    assert render_template("Hi {name}, {{100%}} done", {"name": "Al"}) == "Hi Al, {100%} done"


def test_basic_substitution():
    assert render_template("{a}-{b}", {"a": "x", "b": "y"}) == "x-y"


def test_non_string_values_stringified():
    assert render_template("{n} items, {f}", {"n": 3, "f": 2.5}) == "3 items, 2.5"


def test_empty_template():
    assert render_template("", {"a": 1}) == ""


def test_no_placeholders_copied_verbatim():
    assert render_template("plain text 123", {}) == "plain text 123"


def test_escaped_braces_only():
    assert render_template("{{}}", {}) == "{}"


def test_adjacent_placeholders():
    assert render_template("{a}{b}{a}", {"a": "1", "b": "2"}) == "121"


def test_underscore_and_digits_in_name():
    assert render_template("{user_1}", {"user_1": "ok"}) == "ok"


def test_unicode_preserved_outside_placeholders():
    assert render_template("café {x} ünïcode ", {"x": "☃"}) == "café ☃ ünïcode "


def test_missing_key_raises_keyerror():
    with pytest.raises(KeyError):
        render_template("{missing}", {"a": 1})


def test_missing_key_exact_name():
    with pytest.raises(KeyError) as exc:
        render_template("{foo}", {})
    assert exc.value.args[0] == "foo"


def test_empty_placeholder_raises_valueerror():
    with pytest.raises(ValueError):
        render_template("{}", {})


def test_unterminated_placeholder_raises():
    with pytest.raises(ValueError):
        render_template("{name", {"name": "x"})


def test_illegal_char_in_name_raises():
    with pytest.raises(ValueError):
        render_template("{a b}", {"a b": "x"})


def test_lone_open_brace_raises():
    with pytest.raises(ValueError):
        render_template("a { b", {})


def test_lone_close_brace_raises():
    with pytest.raises(ValueError):
        render_template("a } b", {})


def test_non_ascii_name_is_illegal():
    # 'ä' is not an allowed name character, so this is not a valid placeholder.
    with pytest.raises(ValueError):
        render_template("{äöü}", {"äöü": "x"})


def test_mutation_killer_double_close_not_a_placeholder_terminator():
    # A naive replace-based solution may mishandle the interplay of {{ }} and {name}.
    assert render_template("{{{a}}}", {"a": "V"}) == "{V}"
