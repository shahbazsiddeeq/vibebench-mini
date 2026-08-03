from src.solution import assert_almost_equal
import pytest


def test_passes_for_exact_equal():
    assert assert_almost_equal(1.0, 1.0) is None


def test_message_contains_not_almost_equal():
    with pytest.raises(AssertionError, match="not almost equal"):
        assert_almost_equal(1.0, 1.1)


def test_places_zero_rounds_to_integer():
    assert assert_almost_equal(1.4, 1.4) is None
    with pytest.raises(AssertionError):
        assert_almost_equal(1.0, 2.0, places=0)


def test_round_half_even_at_second_place():
    # round(0.125, 2) == 0.12 (rounds to even), so the diff rounds to a nonzero
    # value and this must raise.
    with pytest.raises(AssertionError):
        assert_almost_equal(0.125, 0.0, places=2)


def test_infinity_raises():
    inf = float("inf")
    # inf - inf is nan (rounds to nan != 0), so equal infinities still raise.
    with pytest.raises(AssertionError):
        assert_almost_equal(inf, inf)
    # inf - 0 is inf, which rounds to inf != 0.
    with pytest.raises(AssertionError):
        assert_almost_equal(inf, 0.0)
