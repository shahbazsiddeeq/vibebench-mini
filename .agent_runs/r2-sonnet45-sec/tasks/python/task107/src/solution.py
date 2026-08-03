def assert_dict_subset(actual, expected):
    """
    Verify that every key/value pair in expected is present in actual with equal value.
    
    Args:
        actual: Dictionary to check against
        expected: Dictionary containing the expected subset of key/value pairs
        
    Returns:
        None if all expected key/value pairs are present in actual
        
    Raises:
        AssertionError: If any expected key is missing or has a different value,
                       with a message reporting all mismatches
    """
    # Validate inputs
    if not isinstance(actual, dict):
        raise TypeError("actual must be a dictionary")
    if not isinstance(expected, dict):
        raise TypeError("expected must be a dictionary")
    
    mismatches = []
    
    for key, expected_value in expected.items():
        if key not in actual:
            # Key is missing from actual
            mismatches.append(f"Missing key: {repr(key)}")
        elif actual[key] != expected_value:
            # Key exists but value differs
            mismatches.append(
                f"Key {repr(key)}: expected {repr(expected_value)}, got {repr(actual[key])}"
            )
    
    if mismatches:
        error_message = "\n".join(mismatches)
        raise AssertionError(error_message)
