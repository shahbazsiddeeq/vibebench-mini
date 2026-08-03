# src/solution.py

def assert_almost_equal(actual, expected, places=7):
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a non-negative integer")
    
    try:
        difference = actual - expected
        if round(difference, places) != 0:
            raise AssertionError("not almost equal")
    except TypeError:
        raise ValueError("Both actual and expected must be numbers")
