from src.solution import normalize_case


def test_basic():
    result = normalize_case("hello world. how are you?")
    assert result == "Hello world. How are you?"


def test_all_caps():
    result = normalize_case("HELLO WORLD.")
    assert result.startswith("Hello")


def test_single_sentence():
    assert normalize_case("hello.") == "Hello."


def test_multiple_punctuation():
    result = normalize_case("hi! how are you? i am fine.")
    assert result == "Hi! How are you? I am fine."


def test_already_normalized():
    s = "Hello world. How are you?"
    assert normalize_case(s.lower()).startswith("Hello")


def test_empty():
    assert normalize_case("") == ""


def test_leading_whitespace():
    # First real letter is capitalized even with leading spaces.
    assert normalize_case("  hello world. bye.") == "  Hello world. Bye."


def test_leading_quote():
    assert normalize_case('"hello world."') == '"Hello world."'


def test_capitalize_after_period_without_space():
    assert normalize_case("hello.world") == "Hello.World"
