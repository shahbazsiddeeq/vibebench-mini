from src.solution import secure_compare


def test_not_equal():
    assert secure_compare("abc", "xyz") is False


def test_different_length():
    assert secure_compare("abc", "ab") is False


def test_same_content_same_case():
    s = "supersecrettoken"
    assert secure_compare(s, s) is True


def test_non_ascii_not_equal():
    assert secure_compare("café", "cafe") is False
