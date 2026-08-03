from src.solution import normalize_url


def test_defaults_to_https_and_lower_host():
    assert normalize_url("Example.com") == "https://example.com/"


def test_sort_query_and_drop_fragment():
    out = normalize_url("https://Ex.com/path?b=2&a=1#frag")
    assert out == "https://ex.com/path?a=1&b=2"


def test_resolves_dot_segments():
    assert normalize_url("https://ex.com/a/./b/../c") == "https://ex.com/a/c"
    assert normalize_url("https://ex.com/x/../../y") == "https://ex.com/y"


def test_scheme_and_path_lowercased_only_host():
    # path case is preserved; only scheme and host are lowercased
    assert normalize_url("HTTPS://Ex.com/PaTh") == "https://ex.com/PaTh"
