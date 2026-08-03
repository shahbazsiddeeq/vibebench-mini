def assert_dict_subset(actual, expected):
    """
    Verify that every key/value pair in expected is present in actual with an equal value.
    Extra keys in actual are ignored.
    
    Raises AssertionError with a message reporting ALL mismatches if expected is not a subset of actual.
    Returns None (passes silently) when expected is a subset.
    
    Args:
        actual: The dictionary to check against
        expected: The dictionary whose key/value pairs should be in actual
        
    Raises:
        AssertionError: If any key/value pair from expected is missing or differs in actual
    """
    # Validate inputs
    if not isinstance(actual, dict):
        raise TypeError("actual must be a dictionary")
    if not isinstance(expected, dict):
        raise TypeError("expected must be a dictionary")
    
    mismatches = []
    
    # Check each key/value pair in expected
    for key, expected_value in expected.items():
        if key not in actual:
            # Key is missing from actual
            mismatches.append(f"Missing key: {key}")
        elif actual[key] != expected_value:
            # Value differs
            mismatches.append(
                f"Key '{key}': expected {expected_value!r} but got {actual[key]!r}"
            )
    
    # If there are any mismatches, raise AssertionError with all of them
    if mismatches:
        error_message = "\n".join(mismatches)
        raise AssertionError(error_message)
