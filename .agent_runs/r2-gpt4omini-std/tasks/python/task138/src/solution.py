# src/solution.py

def assert_almost_equal(actual, expected, places=7):
    if places < 0:
        raise ValueError("places must be non-negative")
    
    if round(actual - expected, places) != 0:
        raise AssertionError("not almost equal")
