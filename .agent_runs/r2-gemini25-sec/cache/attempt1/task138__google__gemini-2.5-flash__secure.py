def assert_almost_equal(actual, expected, places=7):
    """
    Asserts that two values are almost equal within a specified number of decimal places.

    Args:
        actual: The actual value.
        expected: The expected value.
        places: The number of decimal places to round to. Must be a non-negative integer.

    Raises:
        ValueError: If 'places' is negative.
        AssertionError: If the rounded difference between 'actual' and 'expected' is not zero.
    """
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a non-negative integer.")

    try:
        diff = actual - expected
    except TypeError as e:
        raise AssertionError(f"Cannot compare types: {type(actual)} and {type(expected)}") from e

    # Handle NaN results from operations like inf - inf
    if diff != diff:  # Check for NaN
        raise AssertionError(f"{actual} and {expected} are not almost equal (difference is NaN).")

    # Handle infinite differences
    if diff == float('inf') or diff == float('-inf'):
        raise AssertionError(f"{actual} and {expected} are not almost equal (difference is infinite).")

    rounded_diff = round(diff, places)

    if rounded_diff != 0:
        raise AssertionError(f"{actual} and {expected} are not almost equal "
                             f"(difference was {diff}, rounded to {rounded_diff} at {places} places).")
