import pytest

from src.solution import parse_fixed_width

FIELDS = [("name", 0, 7), ("age", 7, 2), ("city", 9, 6)]


def write(tmp_path, text, name="data.txt", newline="\n"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8", newline=newline)
    return str(p)


def test_blank_and_whitespace_lines_skipped(tmp_path):
    p = write(tmp_path, "Alice  30NYC   \n\n   \nBob    25LA    \n")
    assert parse_fixed_width(p, FIELDS) == [
        {"name": "Alice", "age": "30", "city": "NYC"},
        {"name": "Bob", "age": "25", "city": "LA"},
    ]


def test_field_order_preserved(tmp_path):
    p = write(tmp_path, "Alice  30NYC   \n")
    rec = parse_fixed_width(p, FIELDS)[0]
    assert list(rec.keys()) == ["name", "age", "city"]


def test_no_trailing_newline(tmp_path):
    p = write(tmp_path, "Alice  30NYC   ")
    assert parse_fixed_width(p, FIELDS) == [
        {"name": "Alice", "age": "30", "city": "NYC"}
    ]


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        parse_fixed_width(str(tmp_path / "nope.txt"), FIELDS)


def test_negative_start_raises(tmp_path):
    p = write(tmp_path, "anything\n")
    with pytest.raises(ValueError):
        parse_fixed_width(p, [("x", -1, 3)])
