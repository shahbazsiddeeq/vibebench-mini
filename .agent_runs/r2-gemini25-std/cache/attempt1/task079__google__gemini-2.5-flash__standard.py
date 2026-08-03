def validate(data, schema):
    errors = []

    # Check 'required' fields
    if "required" in schema:
        for key in schema["required"]:
            if key not in data:
                errors.append(f"Missing required key: '{key}'")

    # Check 'types' fields
    if "types" in schema:
        type_map = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
        }
        for key, type_name in schema["types"].items():
            if key in data:
                if type_name in type_map:
                    expected_type = type_map[type_name]
                    if not isinstance(data[key], expected_type):
                        errors.append(
                            f"Key '{key}' has incorrect type. Expected '{type_name}', got '{type(data[key]).__name__}'"
                        )
                # else: unknown type_name values are ignored, as per task description

    return errors
