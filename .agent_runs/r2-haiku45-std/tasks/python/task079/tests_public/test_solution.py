from src.solution import validate


def test_missing_required():
    schema = {"required": ["x"]}
    errors = validate({}, schema)
    assert any("x" in e for e in errors)


def test_extra_keys_ok():
    schema = {"required": ["x"]}
    assert validate({"x": 1, "extra": "ok"}, schema) == []


def test_multiple_errors():
    schema = {"required": ["a", "b"], "types": {"c": "str"}}
    errors = validate({"c": 123}, schema)
    assert len(errors) >= 2


def test_list_and_dict_type_mismatch():
    schema = {"types": {"l": "list", "d": "dict"}}
    errors = validate({"l": "notalist", "d": "notadict"}, schema)
    assert len(errors) == 2
