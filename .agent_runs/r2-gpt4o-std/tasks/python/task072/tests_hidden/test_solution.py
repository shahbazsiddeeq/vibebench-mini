import pytest
from src.solution import parse_url


def test_full_url():
    r = parse_url("https://example.com:8080/path?k=v#top")
    assert r["scheme"] == "https"
    assert r["host"] == "example.com"
    assert r["port"] == 8080
    assert r["path"] == "/path"
    assert r["query_params"] == {"k": "v"}
    assert r["fragment"] == "top"


def test_no_query():
    r = parse_url("https://example.com/")
    assert r["query_params"] == {}


def test_missing_scheme_raises():
    with pytest.raises(ValueError):
        parse_url("example.com/path")


def test_repeated_key_becomes_list():
    r = parse_url("https://x.com?a=1&a=2&a=3")
    assert r["query_params"] == {"a": ["1", "2", "3"]}


def test_host_lowercased():
    r = parse_url("https://EXAMPLE.COM/Path")
    assert r["host"] == "example.com"
    # path case is preserved
    assert r["path"] == "/Path"
