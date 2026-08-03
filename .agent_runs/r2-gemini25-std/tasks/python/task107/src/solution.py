def assert_dict_subset(actual, expected):
    """
    Verifies that every key/value pair in expected is present in actual with an equal value;
    extra keys in actual are ignored. It returns None (passes silently) when expected is a subset.
    Otherwise it raises AssertionError whose message reports EVERY mismatch (one per line):
    for a key of expected that is absent from actual the line must contain the substring
    "Missing key" followed by that key; for a key whose value differs the line must contain
    the substring "expected" along with the expected and actual values. All mismatches are
    collected before raising, not just the first.
    """
    mismatches = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: '{key}'")
        elif actual[key] != expected_value:
            mismatches.append(f"Value mismatch for key '{key}': expected {expected_value}, got {actual[key]}")

    if mismatches:
        raise AssertionError("\n".join(mismatches))
