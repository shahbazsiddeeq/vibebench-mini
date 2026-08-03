from __future__ import annotations


def assert_almost_equal(actual: float, expected: float, places: int = 7) -> None:
    """Assert that two floats are equal to within ``places`` decimal places.

    Returns None when round(actual - expected, places) == 0, otherwise raises
    AssertionError with a message containing 'not almost equal'. Raises
    ValueError if places < 0.
    """
    if places < 0:
        raise ValueError("places must be >= 0")

    if round(actual - expected, places) != 0:
        raise AssertionError(
            f"{actual} != {expected} within {places} places (not almost equal)"
        )
    return None
