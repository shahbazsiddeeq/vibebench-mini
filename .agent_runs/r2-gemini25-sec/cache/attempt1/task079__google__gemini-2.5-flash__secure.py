import collections.abc

def validate(data, schema):
    """
    Validates data against a schema dictionary.

    The schema can have two optional keys:
    - "required": A list of keys that must be present in the data.
    - "types": A dictionary mapping keys to their expected type names (e.g., "str", "int").

    Args:
        data: The data (dictionary) to validate.
        schema: The schema (dictionary) to validate against.

    Returns:
        A list of human-readable error messages. Returns an empty list if data is valid.
    """
    errors = []

    if not isinstance(data, dict):
        errors.append("Data must be a dictionary.")
        return errors

    if not isinstance(schema, dict):
        errors.append("Schema must be a dictionary.")
        return errors

    # Validate 'required' fields
    if "required" in schema:
        if not isinstance(schema["required"], list):
            errors.append("Schema 'required' field must be a list.")
        else:
            for key in schema["required"]:
                if not isinstance(key, (str, int, float, bool)): # Basic check for key type
                    errors.append(f"Required key '{key}' is not a valid type for a dictionary key.")
                elif key not in data:
                    errors.append(f"Missing required key: '{key}'")

    # Validate 'types' fields
    if "types" in schema:
        if not isinstance(schema["types"], dict):
            errors.append("Schema 'types' field must be a dictionary.")
        else:
            type_map = {
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
            }
            for key, type_name in schema["types"].items():
                if not isinstance(key, (str, int, float, bool)): # Basic check for key type
                    errors.append(f"Type schema key '{key}' is not a valid type for a dictionary key.")
                    continue

                if key in data:
                    if not isinstance(type_name, str):
                        errors.append(f"Type name for key '{key}' must be a string.")
                        continue

                    if type_name in type_map:
                        expected_type = type_map[type_name]
                        # Special handling for list and dict to use collections.abc for robustness
                        if type_name == "list":
                            if not isinstance(data[key], collections.abc.Sequence) or isinstance(data[key], str):
                                errors.append(f"Key '{key}' must be of type '{type_name}', but got '{type(data[key]).__name__}'.")
                        elif type_name == "dict":
                            if not isinstance(data[key], collections.abc.Mapping):
                                errors.append(f"Key '{key}' must be of type '{type_name}', but got '{type(data[key]).__name__}'.")
                        elif not isinstance(data[key], expected_type):
                            errors.append(f"Key '{key}' must be of type '{type_name}', but got '{type(data[key]).__name__}'.")
                    # Unknown type_name values are ignored as per task description

    return errors
