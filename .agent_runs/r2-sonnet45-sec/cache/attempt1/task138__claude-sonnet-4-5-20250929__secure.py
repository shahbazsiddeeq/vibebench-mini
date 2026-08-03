def assert_almost_equal(actual, expected, places=7):
    """
    Assert that two numbers are almost equal within a given number of decimal places.
    
    Args:
        actual: The actual value (must be a number)
        expected: The expected value (must be a number)
        places: Number of decimal places for rounding (default: 7, must be >= 0)
    
    Returns:
        None if the values are almost equal
    
    Raises:
        ValueError: If places < 0
        AssertionError: If the values are not almost equal
        TypeError: If actual or expected are not numeric types
    """
    # Validate places parameter
    if not isinstance(places, int):
        raise TypeError("places must be an integer")
    if places < 0:
        raise ValueError("places must be non-negative")
    
    # Validate that actual and expected are numeric
    if not isinstance(actual, (int, float)):
        raise TypeError("actual must be a number")
    if not isinstance(expected, (int, float)):
        raise TypeError("expected must be a number")
    
    # Calculate the difference
    diff = actual - expected
    
    # Round the difference to the specified number of places
    rounded_diff = round(diff, places)
    
    # Check if the rounded difference equals zero
    if rounded_diff == 0:
        return None
    else:
        raise AssertionError(f"Values are not almost equal: {actual} != {expected} (difference: {diff}, rounded to {places} places: {rounded_diff})")
