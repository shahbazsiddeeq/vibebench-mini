def assert_almost_equal(actual, expected, places=7):
    """
    Assert that two values are almost equal up to a given number of decimal places.
    
    Args:
        actual: The actual value to compare
        expected: The expected value to compare
        places: Number of decimal places to round to (default 7)
    
    Returns:
        None if the values are almost equal
    
    Raises:
        ValueError: If places < 0
        AssertionError: If the values are not almost equal
    """
    # Validate places parameter
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a non-negative integer")
    
    # Calculate the difference and round it
    difference = actual - expected
    rounded_diff = round(difference, places)
    
    # Check if the rounded difference is zero
    if rounded_diff == 0:
        return None
    
    # Raise AssertionError with appropriate message
    raise AssertionError(
        f"{actual} and {expected} are not almost equal "
        f"(difference: {difference}, rounded to {places} places: {rounded_diff})"
    )
