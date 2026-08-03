# src/solution.py

def validate(data, schema):
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return ["Invalid input: data and schema must be dictionaries."]

    required_keys = schema.get("required", [])
    types = schema.get("types", {})
    
    errors = []

    # Validate required keys
    for key in required_keys:
        if not isinstance(key, str):
            errors.append(f"Invalid key in required: {key}")
            continue
        if key not in data:
            errors.append(f"Missing required key: {key}")

    # Validate types
    type_mapping = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict
    }

    for key, expected_type in types.items():
        if not isinstance(key, str):
            errors.append(f"Invalid key in types: {key}")
            continue
        if expected_type not in type_mapping:
            continue  # Ignore unknown type names
        if key in data and not isinstance(data[key], type_mapping[expected_type]):
            errors.append(f"Type mismatch for key '{key}': expected {expected_type}, got {type(data[key]).__name__}")

    return errors
