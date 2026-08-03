import pytest

from src.solution import parse_csv_line


def test_simple_fields():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]


def test_consecutive_delimiters():
    assert parse_csv_line("a,,b") == ["a", "", "b"]


def test_leading_delimiter_makes_empty_field():
    assert parse_csv_line(",a") == ["", "a"]


def test_escaped_quote_inside_quoted_field():
    assert parse_csv_line('"he said ""hi"""') == ['he said "hi"']


def test_whitespace_preserved():
    assert parse_csv_line("  a , b  ") == ["  a ", " b  "]


def test_custom_delimiter():
    assert parse_csv_line("a;b;c", delimiter=";") == ["a", "b", "c"]


def test_unicode_preserved():
    assert parse_csv_line('café,"π,e",☃') == ["café", "π,e", "☃"]


def test_text_after_closing_quote_raises():
    with pytest.raises(ValueError):
        parse_csv_line('"ab"c')


def test_bad_delimiter_quote_raises():
    with pytest.raises(ValueError):
        parse_csv_line("a,b", delimiter='"')
