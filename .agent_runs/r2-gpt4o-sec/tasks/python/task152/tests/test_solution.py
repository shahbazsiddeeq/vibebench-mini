import pytest

from src.solution import parse_dotenv


def write_env(tmp_path, text):
    p = tmp_path / ".env"
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_example_from_spec(tmp_path):
    p = write_env(
        tmp_path,
        'export NAME="Alice"\n'
        'GREETING="hi\\nthere"\n'
        "PORT=8080  # the port\n"
        "RAW=a#b\n",
    )
    assert parse_dotenv(p) == {
        "NAME": "Alice",
        "GREETING": "hi\nthere",
        "PORT": "8080",
        "RAW": "a#b",
    }


def test_comments_and_blank_lines_skipped(tmp_path):
    p = write_env(tmp_path, "# header comment\n\n   \nA=1\n#B=2\n")
    assert parse_dotenv(p) == {"A": "1"}


def test_single_quotes_are_literal(tmp_path):
    p = write_env(tmp_path, "PATH_VAR='/usr/bin'\nLIT='no\\nescape'\n")
    assert parse_dotenv(p) == {"PATH_VAR": "/usr/bin", "LIT": "no\\nescape"}


def test_double_quote_escapes(tmp_path):
    p = write_env(tmp_path, 'X="a\\tb\\\\c\\"d"\n')
    assert parse_dotenv(p) == {"X": 'a\tb\\c"d'}


def test_double_quote_keeps_inline_hash(tmp_path):
    p = write_env(tmp_path, 'X="a # b"\n')
    assert parse_dotenv(p) == {"X": "a # b"}


def test_unquoted_inline_comment_needs_leading_space(tmp_path):
    p = write_env(tmp_path, "A=foo # comment\nB=foo#bar\nC=#justcomment\n")
    assert parse_dotenv(p) == {"A": "foo", "B": "foo#bar", "C": ""}


def test_empty_value(tmp_path):
    p = write_env(tmp_path, "EMPTY=\n")
    assert parse_dotenv(p) == {"EMPTY": ""}


def test_value_with_equals_sign(tmp_path):
    p = write_env(tmp_path, "URL=key=value&x=1\n")
    assert parse_dotenv(p) == {"URL": "key=value&x=1"}


def test_duplicate_key_last_wins(tmp_path):
    p = write_env(tmp_path, "K=1\nK=2\n")
    assert parse_dotenv(p) == {"K": "2"}


def test_export_prefix_removed(tmp_path):
    p = write_env(tmp_path, "export TOKEN=abc\n")
    assert parse_dotenv(p) == {"TOKEN": "abc"}


def test_missing_equals_raises(tmp_path):
    p = write_env(tmp_path, "NOEQUALS\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)


def test_invalid_key_raises(tmp_path):
    p = write_env(tmp_path, "1BAD=x\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)


def test_empty_key_raises(tmp_path):
    p = write_env(tmp_path, "=value\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        parse_dotenv(str(tmp_path / "nope.env"))
