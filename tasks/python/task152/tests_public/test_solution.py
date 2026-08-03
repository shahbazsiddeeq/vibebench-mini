import pytest

from src.solution import parse_dotenv


def write_env(tmp_path, text):
    p = tmp_path / ".env"
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_comments_and_blank_lines_skipped(tmp_path):
    p = write_env(tmp_path, "# header comment\n\n   \nA=1\n#B=2\n")
    assert parse_dotenv(p) == {"A": "1"}


def test_double_quote_escapes(tmp_path):
    p = write_env(tmp_path, 'X="a\\tb\\\\c\\"d"\n')
    assert parse_dotenv(p) == {"X": 'a\tb\\c"d'}


def test_unquoted_inline_comment_needs_leading_space(tmp_path):
    p = write_env(tmp_path, "A=foo # comment\nB=foo#bar\nC=#justcomment\n")
    assert parse_dotenv(p) == {"A": "foo", "B": "foo#bar", "C": ""}


def test_value_with_equals_sign(tmp_path):
    p = write_env(tmp_path, "URL=key=value&x=1\n")
    assert parse_dotenv(p) == {"URL": "key=value&x=1"}


def test_export_prefix_removed(tmp_path):
    p = write_env(tmp_path, "export TOKEN=abc\n")
    assert parse_dotenv(p) == {"TOKEN": "abc"}


def test_invalid_key_raises(tmp_path):
    p = write_env(tmp_path, "1BAD=x\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        parse_dotenv(str(tmp_path / "nope.env"))
