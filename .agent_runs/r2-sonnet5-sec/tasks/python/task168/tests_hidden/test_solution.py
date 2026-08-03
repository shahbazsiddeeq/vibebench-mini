import pytest

from src.solution import parse_content_type


def test_no_params():
    assert parse_content_type("text/html") == ("text/html", {})


def test_media_type_and_name_lowercased_value_preserved():
    assert parse_content_type('Text/HTML; Charset="UTF-8"') == (
        "text/html",
        {"charset": "UTF-8"},
    )


def test_quoted_value_with_escape():
    assert parse_content_type(r'text/plain; note="a\"b"') == (
        "text/plain",
        {"note": 'a"b'},
    )


def test_duplicate_param_last_wins():
    assert parse_content_type("text/html; x=1; x=2") == (
        "text/html",
        {"x": "2"},
    )


def test_extra_whitespace_trimmed():
    assert parse_content_type("  text/plain ;  charset =  ascii ") == (
        "text/plain",
        {"charset": "ascii"},
    )


def test_invalid_media_type_no_slash():
    with pytest.raises(ValueError):
        parse_content_type("texthtml; charset=utf-8")


def test_param_without_equals_rejected():
    with pytest.raises(ValueError):
        parse_content_type("text/html; charset")


def test_return_type():
    result = parse_content_type("text/html")
    assert type(result) is tuple
    assert type(result[1]) is dict
