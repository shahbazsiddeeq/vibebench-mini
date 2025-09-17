from src.solution import normalize_url


def test_defaults_to_https_and_lower_host():
    assert normalize_url("Example.com") == "https://example.com/"


def test_remove_default_port():
    assert normalize_url("http://EXAMPLE.com:80///a//b") == "http://example.com/a/b"
    assert normalize_url("https://EXAMPLE.com:443") == "https://example.com/"


def test_sort_query_and_drop_fragment():
    out = normalize_url("https://Ex.com/path?b=2&a=1#frag")
    assert out == "https://ex.com/path?a=1&b=2"
