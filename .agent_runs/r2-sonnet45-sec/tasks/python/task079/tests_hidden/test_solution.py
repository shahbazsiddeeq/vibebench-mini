from src.solution import validate


def test_valid_data():
    schema = {"required": ["x"], "types": {"x": "int"}}
    assert validate({"x": 1}, schema) == []


def test_wrong_type():
    schema = {"types": {"x": "int"}}
    errors = validate({"x": "hello"}, schema)
    assert len(errors) == 1


def test_empty_schema():
    assert validate({"any": "thing"}, {}) == []


def test_all_legal_types_accepted():
    schema = {
        "types": {
            "s": "str",
            "i": "int",
            "f": "float",
            "b": "bool",
            "l": "list",
            "d": "dict",
        }
    }
    data = {"s": "x", "i": 1, "f": 1.5, "b": True, "l": [1], "d": {"k": 1}}
    assert validate(data, schema) == []


def test_type_only_checked_when_key_present():
    schema = {"types": {"x": "int"}}
    # "x" absent from data -> no type error (and not required)
    assert validate({}, schema) == []
