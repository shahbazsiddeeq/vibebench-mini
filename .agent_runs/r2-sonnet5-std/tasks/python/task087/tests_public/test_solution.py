from src.solution import parse_cookie


def test_single():
    assert parse_cookie("k=v") == {"k": "v"}


def test_whitespace():
    assert parse_cookie("  k  =  v  ") == {"k": "v"}


def test_no_value():
    result = parse_cookie("k=")
    assert result.get("k") == ""


def test_value_with_equals_signs():
    result = parse_cookie("token=a=b=c")
    assert result == {"token": "a=b=c"}
