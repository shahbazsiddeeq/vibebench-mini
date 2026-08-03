from src.solution import secure_compare


def test_equal_strings():
    assert secure_compare("token123", "token123") is True


def test_empty_equal():
    assert secure_compare("", "") is True


def test_case_sensitive():
    assert secure_compare("ABC", "abc") is False


def test_non_ascii_equal():
    # hmac.compare_digest raises on non-ASCII str; the implementation must
    # encode to bytes first. A naive compare_digest(a, b) would crash here.
    assert secure_compare("café-π-é", "café-π-é") is True


def test_emoji_equal():
    assert secure_compare("token-🔒", "token-🔒") is True
