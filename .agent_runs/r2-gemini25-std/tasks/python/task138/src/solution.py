def assert_almost_equal(actual, expected, places=7):
    """
    Asserts that two values are almost equal.

    Args:
        actual: The actual value.
        expected: The expected value.
        places: The number of decimal places to round to. Defaults to 7.

    Raises:
        ValueError: If places is less than 0.
        AssertionError: If the values are not almost equal after rounding.
    """
    if places < 0:
        raise ValueError("places should be zero or positive")

    diff = actual - expected

    # Handle special floating point values
    if diff != diff:  # Check for NaN
        raise AssertionError(f"{actual} and {expected} are not almost equal (difference is NaN)")
    if diff == float('inf') or diff == float('-inf'):
        raise AssertionError(f"{actual} and {expected} are not almost equal (difference is infinity)")

    if round(diff, places) != 0:
        raise AssertionError(f"{actual} and {expected} are not almost equal (difference was {diff}, rounded to {round(diff, places)} at {places} places)")
