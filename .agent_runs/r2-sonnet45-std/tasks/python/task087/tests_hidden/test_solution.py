from src.solution import parse_cookie


def test_basic():
    result = parse_cookie("session=abc; user=alice")
    assert result == {"session": "abc", "user": "alice"}


def test_empty():
    assert parse_cookie("") == {}


def test_duplicate_last_wins():
    result = parse_cookie("k=1; k=2")
    assert result["k"] == "2"


def test_base64_value_with_padding():
    # base64 padding '=' inside the value must be preserved (split on first '=' only)
    result = parse_cookie("data=YWJjZGVm==; sid=1")
    assert result == {"data": "YWJjZGVm==", "sid": "1"}
