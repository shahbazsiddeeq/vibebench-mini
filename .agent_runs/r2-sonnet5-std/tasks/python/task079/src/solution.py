"""Simple JSON Schema Validator module."""

TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}


def validate(data, schema):
    """Validate `data` against `schema`.

    schema may contain:
      - "required": list of keys that must be present in data
      - "types": dict mapping key -> type_name string

    Returns a list of human-readable error messages.
    """
    errors = []

    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"Missing required key: '{key}'")

    types = schema.get("types", {})
    for key, type_name in types.items():
        if key not in data:
            continue
        expected_type = TYPE_MAP.get(type_name)
        if expected_type is None:
            continue
        value = data[key]
        # bool is a subclass of int, so we need special handling
        if expected_type is int and isinstance(value, bool):
            errors.append(
                f"Key '{key}' expected type 'int', got 'bool'"
            )
        elif expected_type is bool:
            if not isinstance(value, bool):
                errors.append(
                    f"Key '{key}' expected type 'bool', got '{type(value).__name__}'"
                )
        elif not isinstance(value, expected_type):
            errors.append(
                f"Key '{key}' expected type '{type_name}', got '{type(value).__name__}'"
            )

    return errors
