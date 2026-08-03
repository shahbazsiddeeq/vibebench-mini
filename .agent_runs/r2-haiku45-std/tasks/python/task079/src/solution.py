def validate(data, schema):
    """
    Validates data against a schema dict.
    
    Args:
        data: The data to validate (should be a dict)
        schema: A dict with optional "required" (list of keys) and "types" (dict of key->type_name)
    
    Returns:
        A list of error messages (empty if valid)
    """
    errors = []
    
    # Ensure data is a dict
    if not isinstance(data, dict):
        return ["Data must be a dictionary"]
    
    # Check required keys
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    
    # Check types for present keys
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
        # Only check type if key is present in data
        if key in data:
            # Ignore unknown type_name values
            if type_name in type_mapping:
                expected_type = type_mapping[type_name]
                if not isinstance(data[key], expected_type):
                    errors.append(f"Key '{key}' has type {type(data[key]).__name__}, expected {type_name}")
    
    return errors
