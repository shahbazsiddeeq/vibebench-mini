def validate(data, schema):
    """
    Validate data against a schema.
    
    Args:
        data: Dictionary to validate
        schema: Dictionary with optional "required" (list) and "types" (dict) keys
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Input validation
    if not isinstance(data, dict):
        return ["Data must be a dictionary"]
    
    if not isinstance(schema, dict):
        return ["Schema must be a dictionary"]
    
    # Type name to Python type mapping
    type_mapping = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict
    }
    
    # Check required fields
    required = schema.get("required", [])
    if required is not None:
        if not isinstance(required, list):
            return ["Schema 'required' must be a list"]
        
        for key in required:
            if not isinstance(key, str):
                errors.append(f"Required key must be a string, got {type(key).__name__}")
                continue
            if key not in data:
                errors.append(f"Required key '{key}' is missing")
    
    # Check types
    types = schema.get("types", {})
    if types is not None:
        if not isinstance(types, dict):
            return ["Schema 'types' must be a dictionary"]
        
        for key, type_name in types.items():
            # Only check if key exists in data
            if key not in data:
                continue
            
            # Ignore unknown type names
            if type_name not in type_mapping:
                continue
            
            expected_type = type_mapping[type_name]
            actual_value = data[key]
            
            # Check if the value matches the expected type
            if not isinstance(actual_value, expected_type):
                errors.append(
                    f"Key '{key}' has incorrect type: expected {type_name}, "
                    f"got {type(actual_value).__name__}"
                )
    
    return errors
