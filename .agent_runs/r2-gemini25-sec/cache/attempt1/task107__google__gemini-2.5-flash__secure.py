def assert_dict_subset(actual, expected):
    """
    Verifies that every key/value pair in expected is present in actual with an equal value.
    Extra keys in actual are ignored.

    Args:
        actual (dict): The dictionary to check against.
        expected (dict): The dictionary representing the expected subset.

    Raises:
        AssertionError: If expected is not a subset of actual, with a message
                        reporting all mismatches.
    """
    if not isinstance(actual, dict):
        raise TypeError("Input 'actual' must be a dictionary.")
    if not isinstance(expected, dict):
        raise TypeError("Input 'expected' must be a dictionary.")

    mismatches = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: '{key}'")
        else:
            actual_value = actual[key]
            if actual_value != expected_value:
                mismatches.append(
                    f"Value mismatch for key '{key}': expected {repr(expected_value)}, got {repr(actual_value)}"
                )

    if mismatches:
        raise AssertionError("\n".join(mismatches))
