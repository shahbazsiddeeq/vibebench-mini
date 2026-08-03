# src/solution.py

def assert_dict_subset(actual, expected):
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        raise TypeError("Both actual and expected must be dictionaries.")
    
    mismatches = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: {key}")
        elif actual[key] != expected_value:
            mismatches.append(f"expected {expected_value} but got {actual[key]} for key: {key}")

    if mismatches:
        raise AssertionError("\n".join(mismatches))
