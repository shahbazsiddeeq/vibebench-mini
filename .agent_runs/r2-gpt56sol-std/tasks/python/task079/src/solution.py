"""Simple JSON schema validation utilities."""

_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}


def validate(data, schema):
    """Validate a dictionary against a simple schema and return error messages."""
    errors = []

    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"Missing required key: {key}")

    for key, type_name in schema.get("types", {}).items():
        expected_type = _TYPE_MAP.get(type_name)
        if key in data and expected_type is not None:
            if type(data[key]) is not expected_type:
                errors.append(
                    f"Key {key!r} must be of type {type_name}, "
                    f"not {type(data[key]).__name__}"
                )

    return errors
