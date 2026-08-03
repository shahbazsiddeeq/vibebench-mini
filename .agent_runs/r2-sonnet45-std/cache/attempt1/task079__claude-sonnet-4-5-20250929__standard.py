def validate(data, schema):
    """
    Validate data against a schema.
    
    Args:
        data: The data to validate (typically a dict)
        schema: A dict with optional "required" (list) and "types" (dict) keys
        
    Returns:
        A list of error messages (empty if valid)
    """
    errors = []
    
    # Check required fields
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    
    # Check types
    types_schema = schema.get("types", {})
    type_mapping = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict
    }
    
    for key, type_name in types_schema.items():
        # Only check if key exists in data
        if key in data:
            # Only check if type_name is valid (unknown types are ignored)
            if type_name in type_mapping:
                expected_type = type_mapping[type_name]
                if not isinstance(data[key], expected_type):
                    errors.append(f"Key '{key}' has incorrect type: expected {type_name}, got {type(data[key]).__name__}")
    
    return errors
