from src.solution import build_query


def test_empty():
    assert build_query({}) == ""


def test_list_value():
    result = build_query({"tag": ["a", "b"]})
    assert "tag=a" in result and "tag=b" in result


def test_integer_value():
    result = build_query({"n": 42})
    assert "n=42" in result


def test_space_encoded_exact():
    # space encodes as '+' (application/x-www-form-urlencoded)
    assert build_query({"q": "a b"}) == "q=a+b"
