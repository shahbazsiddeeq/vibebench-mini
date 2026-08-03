import pytest
from src.solution import parse_url


def test_no_port():
    r = parse_url("http://example.com/page")
    assert r["port"] is None


def test_no_fragment():
    r = parse_url("https://example.com/")
    assert r["fragment"] == ""


def test_multiple_query_params():
    r = parse_url("https://x.com?a=1&b=2")
    assert r["query_params"]["a"] == "1"
    assert r["query_params"]["b"] == "2"


def test_blank_value_dropped():
    r = parse_url("https://x.com?a=&b=2")
    assert r["query_params"] == {"b": "2"}


def test_full_example_exact():
    assert parse_url("https://example.com:8080/path?k=v#top") == {
        "scheme": "https",
        "host": "example.com",
        "port": 8080,
        "path": "/path",
        "query_params": {"k": "v"},
        "fragment": "top",
    }
