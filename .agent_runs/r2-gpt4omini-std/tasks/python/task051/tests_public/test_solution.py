from src.solution import normalize_case


def test_all_caps():
    result = normalize_case("HELLO WORLD.")
    assert result.startswith("Hello")


def test_multiple_punctuation():
    result = normalize_case("hi! how are you? i am fine.")
    assert result == "Hi! How are you? I am fine."


def test_empty():
    assert normalize_case("") == ""


def test_leading_quote():
    assert normalize_case('"hello world."') == '"Hello world."'
