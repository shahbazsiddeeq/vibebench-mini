import pytest

from src.solution import render_template


def test_worked_example():
    assert render_template("Hi {name}, {{100%}} done", {"name": "Al"}) == "Hi Al, {100%} done"


def test_non_string_values_stringified():
    assert render_template("{n} items, {f}", {"n": 3, "f": 2.5}) == "3 items, 2.5"


def test_no_placeholders_copied_verbatim():
    assert render_template("plain text 123", {}) == "plain text 123"


def test_adjacent_placeholders():
    assert render_template("{a}{b}{a}", {"a": "1", "b": "2"}) == "121"


def test_unicode_preserved_outside_placeholders():
    assert render_template("café {x} ünïcode ", {"x": "☃"}) == "café ☃ ünïcode "


def test_missing_key_exact_name():
    with pytest.raises(KeyError) as exc:
        render_template("{foo}", {})
    assert exc.value.args[0] == "foo"


def test_unterminated_placeholder_raises():
    with pytest.raises(ValueError):
        render_template("{name", {"name": "x"})


def test_lone_open_brace_raises():
    with pytest.raises(ValueError):
        render_template("a { b", {})


def test_non_ascii_name_is_illegal():
    # 'ä' is not an allowed name character, so this is not a valid placeholder.
    with pytest.raises(ValueError):
        render_template("{äöü}", {"äöü": "x"})
