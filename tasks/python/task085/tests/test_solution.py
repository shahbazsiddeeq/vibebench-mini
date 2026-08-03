from src.solution import build_query


def test_basic():
    assert build_query({"b": "2", "a": "1"}) == "a=1&b=2"


def test_empty():
    assert build_query({}) == ""


def test_special_chars_encoded():
    result = build_query({"q": "hello world"})
    assert "+" in result or "%20" in result


def test_list_value():
    result = build_query({"tag": ["a", "b"]})
    assert "tag=a" in result and "tag=b" in result


def test_sorted_keys():
    result = build_query({"z": "1", "a": "2", "m": "3"})
    keys = [p.split("=")[0] for p in result.split("&")]
    assert keys == sorted(keys)


def test_integer_value():
    result = build_query({"n": 42})
    assert "n=42" in result


def test_sorted_with_list_value_exact():
    # keys sorted; a list expands to repeated keys in order
    assert build_query({"z": ["1", "2"], "a": "x"}) == "a=x&z=1&z=2"


def test_space_encoded_exact():
    # space encodes as '+' (application/x-www-form-urlencoded)
    assert build_query({"q": "a b"}) == "q=a+b"


def test_reserved_chars_encoded_exact():
    assert build_query({"k": "a&b=c"}) == "k=a%26b%3Dc"
