from numbers import Real


def assert_almost_equal(actual, expected, places=7):
    """
    Assert that two numbers are almost equal, comparing their difference
    rounded to a given number of decimal places.

    Returns None if round(actual - expected, places) == 0.
    Raises AssertionError with a message containing 'not almost equal' otherwise.
    Raises ValueError if places < 0 or if inputs are of invalid type.
    """
    if isinstance(places, bool) or not isinstance(places, int):
        raise ValueError("places must be a non-negative integer")
    if places < 0:
        raise ValueError("places must be a non-negative integer")

    if isinstance(actual, bool) or not isinstance(actual, Real):
        raise ValueError("actual must be a real number")
    if isinstance(expected, bool) or not isinstance(expected, Real):
        raise ValueError("expected must be a real number")

    actual = float(actual)
    expected = float(expected)

    diff = actual - expected
    rounded_diff = round(diff, places)

    if rounded_diff == 0:
        return None

    raise AssertionError(
        f"{actual!r} != {expected!r} within {places} places: values are not almost equal "
        f"(difference rounded to {rounded_diff!r})"
    )
