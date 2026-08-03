def assert_dict_subset(actual, expected):
    """
    Verify that every key/value pair in `expected` is present in `actual`
    with an equal value. Extra keys in `actual` are ignored.

    Raises AssertionError with a message reporting every mismatch found.
    """
    errors = []

    for key, expected_value in expected.items():
        if key not in actual:
            errors.append(f"Missing key: {key!r}")
        else:
            actual_value = actual[key]
            if actual_value != expected_value:
                errors.append(
                    f"Value mismatch for key {key!r}: expected {expected_value!r}, "
                    f"got {actual_value!r}"
                )

    if errors:
        raise AssertionError("\n".join(errors))
