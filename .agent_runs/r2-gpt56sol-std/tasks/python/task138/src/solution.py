def assert_almost_equal(actual, expected, places=7):
    """Assert that actual and expected are equal when their difference is rounded."""
    if places < 0:
        raise ValueError("places must be non-negative")

    if round(actual - expected, places) != 0:
        raise AssertionError(f"{actual!r} and {expected!r} are not almost equal")

    return None
