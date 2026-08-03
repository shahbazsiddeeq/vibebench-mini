def assert_almost_equal(actual, expected, places=7):
    """
    Assert that actual and expected are almost equal.
    
    Returns None if round(actual - expected, places) == 0,
    otherwise raises AssertionError with a message containing 'not almost equal'.
    Raises ValueError if places < 0.
    
    Args:
        actual: The actual value
        expected: The expected value
        places: Number of decimal places (default 7)
    
    Returns:
        None if values are almost equal
        
    Raises:
        AssertionError: If values are not almost equal
        ValueError: If places < 0
    """
    if places < 0:
        raise ValueError("places must be non-negative")
    
    diff = actual - expected
    rounded_diff = round(diff, places)
    
    if rounded_diff == 0:
        return None
    else:
        raise AssertionError(f"{actual} and {expected} are not almost equal")
