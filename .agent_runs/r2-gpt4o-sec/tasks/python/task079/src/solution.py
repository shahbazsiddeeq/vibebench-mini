# src/solution.py

def validate(data, schema):
    errors = []

    # Validate required fields
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate types
    type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict
    }
    
    types = schema.get("types", {})
    for field, type_name in types.items():
        if field in data:
            expected_type = type_map.get(type_name)
            if expected_type and not isinstance(data[field], expected_type):
                errors.append(f"Field '{field}' is not of type '{type_name}'")

    return errors
