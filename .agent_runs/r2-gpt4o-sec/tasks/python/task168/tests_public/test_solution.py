import pytest

from src.solution import parse_content_type


def test_simple_charset():
    assert parse_content_type("text/html; charset=utf-8") == (
        "text/html",
        {"charset": "utf-8"},
    )


def test_quoted_value_with_semicolon():
    # Mutation killer: a naive .split(';') breaks the value 'a;b' into two.
    assert parse_content_type('multipart/form-data; name="a;b"') == (
        "multipart/form-data",
        {"name": "a;b"},
    )


def test_multiple_params():
    assert parse_content_type("application/json; a=1; b=2") == (
        "application/json",
        {"a": "1", "b": "2"},
    )


def test_empty_and_trailing_semicolons_skipped():
    assert parse_content_type("text/html;; charset=utf-8;") == (
        "text/html",
        {"charset": "utf-8"},
    )


def test_unquoted_value_case_preserved():
    assert parse_content_type("text/plain; boundary=AaBbCc") == (
        "text/plain",
        {"boundary": "AaBbCc"},
    )


def test_invalid_media_type_empty_subtype():
    with pytest.raises(ValueError):
        parse_content_type("text/; charset=utf-8")


def test_worked_example():
    assert parse_content_type('Text/HTML; Charset="UTF-8"; boundary=--x') == (
        "text/html",
        {"charset": "UTF-8", "boundary": "--x"},
    )
