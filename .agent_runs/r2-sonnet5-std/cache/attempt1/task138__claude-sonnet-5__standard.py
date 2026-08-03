def assert_almost_equal(actual, expected, places=7):
    if places < 0:
        raise ValueError("places must be >= 0")
    diff = round(actual - expected, places)
    if diff != 0:
        raise AssertionError(
            f"{actual!r} != {expected!r} within {places} places, "
            f"values are not almost equal"
        )
    return None
