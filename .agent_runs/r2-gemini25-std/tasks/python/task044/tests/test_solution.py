from src.solution import to_camel, to_snake


def test_camel_to_snake():
    assert to_snake("myVariableName") == "my_variable_name"


def test_snake_to_camel():
    assert to_camel("my_variable_name") == "myVariableName"


def test_already_snake():
    assert to_snake("my_var") == "my_var"


def test_two_part_snake():
    assert to_camel("my_var") == "myVar"


def test_empty():
    assert to_snake("") == ""
    assert to_camel("") == ""


def test_single_word():
    assert to_snake("hello") == "hello"
    assert to_camel("hello") == "hello"


def test_acronym():
    assert to_snake("parseHTML") == "parse_html"


def test_acronym_leading():
    assert to_snake("HTMLParser") == "html_parser"


def test_camel_lowercases_first_letter():
    # An uppercase leading part must still yield a lowercase first letter.
    assert to_camel("My_var") == "myVar"
    assert to_camel("HELLO_world") == "helloWorld"


def test_roundtrip():
    original = "my_variable_name"
    assert to_snake(to_camel(original)) == original
