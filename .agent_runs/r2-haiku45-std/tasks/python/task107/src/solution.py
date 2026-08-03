def assert_dict_subset(actual, expected):
    """
    Verifies that every key/value pair in expected is present in actual with an equal value.
    Extra keys in actual are ignored.
    
    Raises AssertionError with a message reporting ALL mismatches if expected is not a subset of actual.
    """
    mismatches = []
    
    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: {key}")
        elif actual[key] != expected_value:
            mismatches.append(f"Key '{key}': expected {expected_value}, but got {actual[key]}")
    
    if mismatches:
        raise AssertionError("\n".join(mismatches))
