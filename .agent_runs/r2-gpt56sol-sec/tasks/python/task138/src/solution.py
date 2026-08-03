"""Numeric assertion helpers."""


def assert_almost_equal(actual, expected, places=7):
    """Assert that the difference rounds to zero at the given precision."""
    if places < 0:
        raise ValueError("places must be non-negative")

    if round(actual - expected, places) != 0:
        raise AssertionError("values are not almost equal")

    return None
