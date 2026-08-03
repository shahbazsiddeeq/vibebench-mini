def assert_dict_subset(actual: dict, expected: dict) -> None:
    errors = []
    for key, exp_val in expected.items():
        if key not in actual:
            errors.append(f"Missing key: {key!r}")
        elif actual[key] != exp_val:
            errors.append(f"Key {key!r}: expected {exp_val!r}, got {actual[key]!r}")
    if errors:
        raise AssertionError("\n".join(errors))
