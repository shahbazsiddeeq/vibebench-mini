from src.solution import secure_compare


def test_equal_strings():
    assert secure_compare("token123", "token123") is True


def test_not_equal():
    assert secure_compare("abc", "xyz") is False


def test_empty_equal():
    assert secure_compare("", "") is True


def test_different_length():
    assert secure_compare("abc", "ab") is False


def test_case_sensitive():
    assert secure_compare("ABC", "abc") is False


def test_same_content_same_case():
    s = "supersecrettoken"
    assert secure_compare(s, s) is True


def test_non_ascii_equal():
    # hmac.compare_digest raises on non-ASCII str; the implementation must
    # encode to bytes first. A naive compare_digest(a, b) would crash here.
    assert secure_compare("café-π-é", "café-π-é") is True


def test_non_ascii_not_equal():
    assert secure_compare("café", "cafe") is False


def test_emoji_equal():
    assert secure_compare("token-🔒", "token-🔒") is True
