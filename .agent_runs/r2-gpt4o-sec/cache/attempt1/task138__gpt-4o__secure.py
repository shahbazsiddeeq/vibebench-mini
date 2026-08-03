# src/solution.py

import math

def assert_almost_equal(actual, expected, places=7):
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a non-negative integer")
    
    if not (isinstance(actual, (int, float)) and isinstance(expected, (int, float))):
        raise TypeError("actual and expected must be numbers")
    
    difference = actual - expected
    
    # Check for NaN or infinity
    if math.isnan(difference) or math.isinf(difference):
        raise AssertionError("Values are not almost equal: difference is NaN or infinity")
    
    if round(difference, places) != 0:
        raise AssertionError(f"Values are not almost equal: {actual} and {expected} differ by {difference}")
    
    return None
