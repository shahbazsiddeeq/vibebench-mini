# src/solution.py

def assert_almost_equal(actual, expected, places=7):
    if places < 0:
        raise ValueError("places must be non-negative")
    
    difference = actual - expected
    if round(difference, places) != 0:
        raise AssertionError(f"{actual} and {expected} are not almost equal to {places} decimal places")
