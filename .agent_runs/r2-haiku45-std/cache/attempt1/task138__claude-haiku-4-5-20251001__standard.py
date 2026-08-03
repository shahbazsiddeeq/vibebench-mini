def assert_almost_equal(actual, expected, places=7):
    """
    Assert that actual and expected are almost equal.
    
    Returns None if round(actual - expected, places) == 0.
    Raises AssertionError if they are not almost equal.
    Raises ValueError if places < 0.
    """
    if places < 0:
        raise ValueError("places must be >= 0")
    
    diff = actual - expected
    rounded_diff = round(diff, places)
    
    if rounded_diff == 0:
        return None
    else:
        raise AssertionError(f"{actual} not almost equal to {expected} within {places} places")
