from src.solution import assert_almost_equal
import pytest


def test_passes_for_float_rounding():
    assert assert_almost_equal(0.1 + 0.2, 0.3) is None


def test_raises_when_far_apart():
    with pytest.raises(AssertionError):
        assert_almost_equal(1.0, 2.0)


def test_places_controls_tolerance():
    # Differ at the 2nd decimal place.
    assert assert_almost_equal(1.001, 1.002, places=2) is None
    with pytest.raises(AssertionError):
        assert_almost_equal(1.001, 1.002, places=3)


def test_round_half_even_boundary_passes():
    # diff == 0.5, places=0: round(0.5, 0) is 0.0 under banker's rounding, so
    # this passes. A tolerance defined as abs(diff) < 0.5 would (wrongly) raise.
    assert assert_almost_equal(0.5, 0.0, places=0) is None
    assert assert_almost_equal(-0.5, 0.0, places=0) is None


def test_nan_is_never_almost_equal():
    nan = float("nan")
    # round(nan - nan, places) is nan, and nan != 0, so this raises.
    with pytest.raises(AssertionError):
        assert_almost_equal(nan, nan)
    with pytest.raises(AssertionError):
        assert_almost_equal(nan, 1.0)


def test_negative_places_raises_value_error():
    with pytest.raises(ValueError):
        assert_almost_equal(1.0, 1.0, places=-1)
