import pytest

from src.solution import parse_csv_line


def test_worked_example():
    assert parse_csv_line('a,"b,c","d""e",') == ["a", "b,c", 'd"e', ""]


def test_simple_fields():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]


def test_empty_line_yields_one_empty_field():
    assert parse_csv_line("") == [""]


def test_consecutive_delimiters():
    assert parse_csv_line("a,,b") == ["a", "", "b"]


def test_trailing_delimiter_makes_empty_field():
    assert parse_csv_line("a,b,") == ["a", "b", ""]


def test_leading_delimiter_makes_empty_field():
    assert parse_csv_line(",a") == ["", "a"]


def test_quoted_field_contains_delimiter():
    assert parse_csv_line('"x,y",z') == ["x,y", "z"]


def test_escaped_quote_inside_quoted_field():
    assert parse_csv_line('"he said ""hi"""') == ['he said "hi"']


def test_quoted_empty_field():
    assert parse_csv_line('"",a') == ["", "a"]


def test_whitespace_preserved():
    assert parse_csv_line("  a , b  ") == ["  a ", " b  "]


def test_quote_literal_in_unquoted_field():
    assert parse_csv_line('a"b,c') == ['a"b', "c"]


def test_custom_delimiter():
    assert parse_csv_line("a;b;c", delimiter=";") == ["a", "b", "c"]


def test_custom_delimiter_with_quotes():
    assert parse_csv_line('"a;b";c', delimiter=";") == ["a;b", "c"]


def test_unicode_preserved():
    assert parse_csv_line('café,"π,e",☃') == ["café", "π,e", "☃"]


def test_unterminated_quote_raises():
    with pytest.raises(ValueError):
        parse_csv_line('"abc')


def test_text_after_closing_quote_raises():
    with pytest.raises(ValueError):
        parse_csv_line('"ab"c')


def test_bad_delimiter_multichar_raises():
    with pytest.raises(ValueError):
        parse_csv_line("a,b", delimiter=",,")


def test_bad_delimiter_quote_raises():
    with pytest.raises(ValueError):
        parse_csv_line("a,b", delimiter='"')


def test_mutation_killer_quote_only_special_at_field_start():
    # The quote is special only as the first char of a field; here it is not,
    # so it must stay literal and the comma still splits.
    assert parse_csv_line('1,2"3,4') == ["1", '2"3', "4"]
