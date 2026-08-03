def assert_dict_subset(actual, expected):
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        raise TypeError("Both actual and expected must be dictionaries.")

    mismatches = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: {key}")
        elif actual[key] != expected_value:
            mismatches.append(f"Key '{key}': expected {expected_value}, got {actual[key]}")

    if mismatches:
        raise AssertionError("\n".join(mismatches))
