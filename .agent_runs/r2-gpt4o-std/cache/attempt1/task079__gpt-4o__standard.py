# src/solution.py

def validate(data, schema):
    errors = []

    # Check for required keys
    required_keys = schema.get("required", [])
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")

    # Check for type mismatches
    type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict
    }
    
    types = schema.get("types", {})
    for key, expected_type_name in types.items():
        if key in data:
            expected_type = type_map.get(expected_type_name)
            if expected_type and not isinstance(data[key], expected_type):
                errors.append(f"Key '{key}' expected type '{expected_type_name}', got '{type(data[key]).__name__}'")

    return errors
