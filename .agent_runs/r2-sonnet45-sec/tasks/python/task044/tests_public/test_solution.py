from src.solution import to_camel, to_snake


def test_snake_to_camel():
    assert to_camel("my_variable_name") == "myVariableName"


def test_two_part_snake():
    assert to_camel("my_var") == "myVar"


def test_single_word():
    assert to_snake("hello") == "hello"
    assert to_camel("hello") == "hello"


def test_acronym_leading():
    assert to_snake("HTMLParser") == "html_parser"


def test_roundtrip():
    original = "my_variable_name"
    assert to_snake(to_camel(original)) == original
