from src.solution import assert_almost_equal
import pytest


def test_passes_for_float_rounding():
    assert assert_almost_equal(0.1 + 0.2, 0.3) is None


def test_passes_for_exact_equal():
    assert assert_almost_equal(1.0, 1.0) is None


def test_raises_when_far_apart():
    with pytest.raises(AssertionError):
        assert_almost_equal(1.0, 2.0)


def test_message_contains_not_almost_equal():
    with pytest.raises(AssertionError, match="not almost equal"):
        assert_almost_equal(1.0, 1.1)


def test_places_controls_tolerance():
    # Differ at the 2nd decimal place.
    assert assert_almost_equal(1.001, 1.002, places=2) is None
    with pytest.raises(AssertionError):
        assert_almost_equal(1.001, 1.002, places=3)


def test_places_zero_rounds_to_integer():
    assert assert_almost_equal(1.4, 1.4) is None
    with pytest.raises(AssertionError):
        assert_almost_equal(1.0, 2.0, places=0)


def test_round_half_even_boundary_passes():
    # diff == 0.5, places=0: round(0.5, 0) is 0.0 under banker's rounding, so
    # this passes. A tolerance defined as abs(diff) < 0.5 would (wrongly) raise.
    assert assert_almost_equal(0.5, 0.0, places=0) is None
    assert assert_almost_equal(-0.5, 0.0, places=0) is None


def test_round_half_even_at_second_place():
    # round(0.125, 2) == 0.12 (rounds to even), so the diff rounds to a nonzero
    # value and this must raise.
    with pytest.raises(AssertionError):
        assert_almost_equal(0.125, 0.0, places=2)


def test_nan_is_never_almost_equal():
    nan = float("nan")
    # round(nan - nan, places) is nan, and nan != 0, so this raises.
    with pytest.raises(AssertionError):
        assert_almost_equal(nan, nan)
    with pytest.raises(AssertionError):
        assert_almost_equal(nan, 1.0)


def test_infinity_raises():
    inf = float("inf")
    # inf - inf is nan (rounds to nan != 0), so equal infinities still raise.
    with pytest.raises(AssertionError):
        assert_almost_equal(inf, inf)
    # inf - 0 is inf, which rounds to inf != 0.
    with pytest.raises(AssertionError):
        assert_almost_equal(inf, 0.0)


def test_negative_places_raises_value_error():
    with pytest.raises(ValueError):
        assert_almost_equal(1.0, 1.0, places=-1)
