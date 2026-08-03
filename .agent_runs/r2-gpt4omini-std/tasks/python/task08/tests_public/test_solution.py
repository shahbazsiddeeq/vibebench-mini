from src.solution import normalize_url


def test_remove_default_port():
    assert normalize_url("http://EXAMPLE.com:80///a//b") == "http://example.com/a/b"
    assert normalize_url("https://EXAMPLE.com:443") == "https://example.com/"


def test_preserves_userinfo_case_and_lowercases_host():
    assert normalize_url("http://User:Pass@Host.COM/") == "http://User:Pass@host.com/"


def test_blank_query_value_kept_and_sorted():
    assert normalize_url("https://ex.com/?b=2&a=") == "https://ex.com/?a=&b=2"
