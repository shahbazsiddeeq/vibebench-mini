def assert_dict_subset(actual, expected):
    """
    Verify that every key/value pair in expected is present in actual with equal value.
    
    Args:
        actual: The dictionary being tested
        expected: The dictionary containing expected key/value pairs
        
    Returns:
        None if all expected key/value pairs are present in actual
        
    Raises:
        AssertionError: If any expected key is missing or has a different value in actual
    """
    mismatches = []
    
    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: {key}")
        elif actual[key] != expected_value:
            mismatches.append(
                f"Key {key}: expected {expected_value}, got {actual[key]}"
            )
    
    if mismatches:
        raise AssertionError("\n".join(mismatches))
