"""Simple JSON Schema Validator module."""


def validate(data, schema):
    """
    Validate data against a schema.
    
    Args:
        data: The data to validate (should be a dict)
        schema: The schema dict with optional "required" and "types" keys
        
    Returns:
        A list of human-readable error messages for violations
    """
    errors = []
    
    # Input validation
    if not isinstance(data, dict):
        return ["Data must be a dictionary"]
    
    if not isinstance(schema, dict):
        return ["Schema must be a dictionary"]
    
    # Type mapping from string names to Python types
    type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
    }
    
    # Check required fields
    required = schema.get("required", [])
    if isinstance(required, list):
        for key in required:
            if not isinstance(key, str):
                continue
            if key not in data:
                errors.append(f"Missing required key: {key}")
    
    # Check types for present keys
    types_schema = schema.get("types", {})
    if isinstance(types_schema, dict):
        for key, type_name in types_schema.items():
            if not isinstance(key, str) or not isinstance(type_name, str):
                continue
            
            # Only check type if key is present in data
            if key in data:
                # Ignore unknown type names
                if type_name not in type_map:
                    continue
                
                expected_type = type_map[type_name]
                actual_value = data[key]
                
                # Special handling for bool: bool is a subclass of int in Python,
                # so we need to check bool explicitly before int
                if type_name == "bool":
                    if not isinstance(actual_value, bool):
                        errors.append(
                            f"Key '{key}' has type {type(actual_value).__name__}, "
                            f"expected bool"
                        )
                elif type_name == "int":
                    # Reject bool values for int type
                    if isinstance(actual_value, bool) or not isinstance(actual_value, int):
                        errors.append(
                            f"Key '{key}' has type {type(actual_value).__name__}, "
                            f"expected int"
                        )
                else:
                    if not isinstance(actual_value, expected_type):
                        errors.append(
                            f"Key '{key}' has type {type(actual_value).__name__}, "
                            f"expected {type_name}"
                        )
    
    return errors
