from src.solution import validate


def test_valid_data():
    schema = {"required": ["x"], "types": {"x": "int"}}
    assert validate({"x": 1}, schema) == []


def test_missing_required():
    schema = {"required": ["x"]}
    errors = validate({}, schema)
    assert any("x" in e for e in errors)


def test_wrong_type():
    schema = {"types": {"x": "int"}}
    errors = validate({"x": "hello"}, schema)
    assert len(errors) == 1


def test_extra_keys_ok():
    schema = {"required": ["x"]}
    assert validate({"x": 1, "extra": "ok"}, schema) == []


def test_empty_schema():
    assert validate({"any": "thing"}, {}) == []


def test_multiple_errors():
    schema = {"required": ["a", "b"], "types": {"c": "str"}}
    errors = validate({"c": 123}, schema)
    assert len(errors) >= 2


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


def test_list_and_dict_type_mismatch():
    schema = {"types": {"l": "list", "d": "dict"}}
    errors = validate({"l": "notalist", "d": "notadict"}, schema)
    assert len(errors) == 2


def test_type_only_checked_when_key_present():
    schema = {"types": {"x": "int"}}
    # "x" absent from data -> no type error (and not required)
    assert validate({}, schema) == []
