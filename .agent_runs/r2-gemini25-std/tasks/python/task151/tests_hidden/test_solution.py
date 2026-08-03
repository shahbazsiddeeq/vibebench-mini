import pytest

from src.solution import parse_fixed_width

FIELDS = [("name", 0, 7), ("age", 7, 2), ("city", 9, 6)]


def write(tmp_path, text, name="data.txt", newline="\n"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8", newline=newline)
    return str(p)


def test_basic_two_records(tmp_path):
    p = write(tmp_path, "Alice  30NYC   \nBob    25LA    \n")
    assert parse_fixed_width(p, FIELDS) == [
        {"name": "Alice", "age": "30", "city": "NYC"},
        {"name": "Bob", "age": "25", "city": "LA"},
    ]


def test_short_line_yields_available_chars(tmp_path):
    p = write(tmp_path, "Al     7\n")
    result = parse_fixed_width(p, FIELDS)
    assert result == [{"name": "Al", "age": "7", "city": ""}]


def test_crlf_newlines(tmp_path):
    # newline='' keeps the literal \r\n we write.
    p = write(tmp_path, "Alice  30NYC   \r\nBob    25LA    \r\n", newline="")
    assert parse_fixed_width(p, FIELDS) == [
        {"name": "Alice", "age": "30", "city": "NYC"},
        {"name": "Bob", "age": "25", "city": "LA"},
    ]


def test_utf8_content(tmp_path):
    p = write(tmp_path, "José   28\n", newline="\n")
    fields = [("name", 0, 7), ("age", 7, 2)]
    assert parse_fixed_width(p, fields) == [{"name": "José", "age": "28"}]


def test_empty_fields_raises(tmp_path):
    p = write(tmp_path, "anything\n")
    with pytest.raises(ValueError):
        parse_fixed_width(p, [])


def test_zero_length_raises(tmp_path):
    p = write(tmp_path, "anything\n")
    with pytest.raises(ValueError):
        parse_fixed_width(p, [("x", 0, 0)])
