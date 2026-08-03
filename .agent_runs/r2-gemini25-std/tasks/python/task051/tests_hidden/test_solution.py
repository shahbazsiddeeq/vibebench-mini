from src.solution import normalize_case


def test_basic():
    result = normalize_case("hello world. how are you?")
    assert result == "Hello world. How are you?"


def test_single_sentence():
    assert normalize_case("hello.") == "Hello."


def test_already_normalized():
    s = "Hello world. How are you?"
    assert normalize_case(s.lower()).startswith("Hello")


def test_leading_whitespace():
    # First real letter is capitalized even with leading spaces.
    assert normalize_case("  hello world. bye.") == "  Hello world. Bye."


def test_capitalize_after_period_without_space():
    assert normalize_case("hello.world") == "Hello.World"
