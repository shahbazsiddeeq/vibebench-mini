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


def test_single_quotes_are_literal(tmp_path):
    p = write_env(tmp_path, "PATH_VAR='/usr/bin'\nLIT='no\\nescape'\n")
    assert parse_dotenv(p) == {"PATH_VAR": "/usr/bin", "LIT": "no\\nescape"}


def test_double_quote_keeps_inline_hash(tmp_path):
    p = write_env(tmp_path, 'X="a # b"\n')
    assert parse_dotenv(p) == {"X": "a # b"}


def test_empty_value(tmp_path):
    p = write_env(tmp_path, "EMPTY=\n")
    assert parse_dotenv(p) == {"EMPTY": ""}


def test_duplicate_key_last_wins(tmp_path):
    p = write_env(tmp_path, "K=1\nK=2\n")
    assert parse_dotenv(p) == {"K": "2"}


def test_missing_equals_raises(tmp_path):
    p = write_env(tmp_path, "NOEQUALS\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)


def test_empty_key_raises(tmp_path):
    p = write_env(tmp_path, "=value\n")
    with pytest.raises(ValueError):
        parse_dotenv(p)
